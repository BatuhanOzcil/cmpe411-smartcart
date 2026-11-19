"""Small, reproducible mutation experiment for SmartCart.

This is NOT a full mutation-testing engine. For each selected mutation, copy
source and tests to a temporary folder, apply ONE change, and run pytest.
Never changes the original project or Git working tree.

Run: python3 tools/check_mutations.py
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# name, exact original source fragment, deliberately wrong replacement
MUTANTS = [
    (
        "M1_coupon_500_off_by_one",
        'subtotal >= COUPON_MINIMUM:',
        'subtotal > COUPON_MINIMUM:',
    ),
    (
        "M2_member_rate_6_percent",
        'MEMBER_RATE = Decimal("0.05")',
        'MEMBER_RATE = Decimal("0.06")',
    ),
    (
        "M3_coupon_rate_9_percent",
        'COUPON_RATE = Decimal("0.10")',
        'COUPON_RATE = Decimal("0.09")',
    ),
    (
        "M4_quantity_max_plus_one",
        '1 <= qty <= MAX_QUANTITY:',
        '1 <= qty <= MAX_QUANTITY + 1:',
    ),
    (
        "M5_price_max_plus_one_cent",
        'amount > MAX_UNIT_PRICE:',
        'amount > MAX_UNIT_PRICE + CENT:',
    ),
    (
        "M6_cart_size_plus_one",
        '1 <= len(items) <= MAX_CART_ITEMS:',
        '1 <= len(items) <= MAX_CART_ITEMS + 1:',
    ),
    (
        "M7_disable_coupon_validation",
        'if coupon not in (None, "SAVE10"):',
        'if False:',
    ),
    (
        "M8_incorrect_quantity_subtotal",
        'subtotal += unit_price * qty',
        'subtotal += unit_price',
    ),
    (
        "M9_bankers_rounding_instead_of_half_up",
        'rounding=ROUND_HALF_UP',
        'rounding="ROUND_HALF_EVEN"',
    ),
]


SUPPLEMENTAL_MUTANTS = [
    (
        "M10_coupon_only_half_even",
        "cart.py",
        "(subtotal * rate).quantize(CENT, rounding=ROUND_HALF_UP)",
        '(subtotal * rate).quantize(CENT, rounding="ROUND_HALF_EVEN" '
        'if applied == "SAVE10" else ROUND_HALF_UP)',
    ),
    (
        "M11_lose_member_fallback",
        "cart.py",
        "elif is_member:",
        "elif is_member and coupon is None:",
    ),
    (
        "M12_api_default_member_true",
        "api.py",
        "Field(default=False, strict=True)",
        "Field(default=True, strict=True)",
    ),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "tests", nargs="*", help="Test paths or node IDs relative to the repository root."
    )
    parser.add_argument(
        "--supplemental", action="store_true", help="Run the three supplemental mutants instead."
    )
    args = parser.parse_args()
    mutations = (
        SUPPLEMENTAL_MUTANTS
        if args.supplemental
        else [(name, "cart.py", original, replacement) for name, original, replacement in MUTANTS]
    )
    command = [sys.executable, "-m", "pytest", "-q", "--disable-warnings", *args.tests]
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    clean = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True, timeout=30)
    if clean.returncode:
        print("ERROR: the selected tests must pass on the unmodified code.")
        print(clean.stdout + clean.stderr)
        return 1

    killed = 0
    survived = 0
    broken = 0
    for name, filename, original, replacement in mutations:
        source = (ROOT / filename).read_text(encoding="utf-8")
        if source.count(original) != 1:
            print(f"ERROR {name}: source text is not uniquely matched")
            broken += 1
            continue
        with tempfile.TemporaryDirectory(prefix="smartcart_mutant_") as tmp:
            work = Path(tmp)
            for source_file in ("cart.py", "api.py", "pytest.ini"):
                shutil.copy2(ROOT / source_file, work / source_file)
            (work / filename).write_text(source.replace(original, replacement, 1), encoding="utf-8")
            shutil.copytree(
                ROOT / "tests", work / "tests",
                ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"),
            )
            try:
                result = subprocess.run(
                    command, cwd=work, env=env, capture_output=True, text=True, timeout=30,
                )
            except subprocess.TimeoutExpired:
                print(f"ERROR {name}: pytest timed out")
                broken += 1
                continue
            summary = (result.stdout + "\n" + result.stderr).splitlines()
            last = next(
                (line.strip() for line in reversed(summary)
                 if re.search(r"\b(passed|failed|error|errors)\b", line)),
                "no summary",
            )
            if result.returncode == 0:
                survived += 1
                state = "SURVIVED"
            elif (
                result.returncode == 1
                and re.search(r"\b\d+ failed\b", last)
                and not re.search(r"\b\d+ errors?\b", last)
            ):
                killed += 1
                state = "KILLED"
            else:
                broken += 1
                state = "ERROR"  # A crash/collection issue is NOT a meaningful kill.
            print(f"{name}: {state} | {last}")
            for line in summary:
                if line.startswith("FAILED "):
                    print(f"  {line.split(' - ', 1)[0]}")

    total_valid = killed + survived
    print(f"\nValid mutants: {total_valid} | killed: {killed} | survived: {survived} | errors: {broken}")
    print(f"Observed kill rate on this selected set: {killed / total_valid:.1%}" if total_valid else "No valid mutants")
    print("Note: This selected sample is not a whole-code mutation score.")
    return 1 if broken else 0


if __name__ == "__main__":
    raise SystemExit(main())
