# Lab 3 progress — original published date: 20 November 2026

Official Project Brief: **show at least 10 running automated tests** in Lab 3. It says "in the lab, not graded" for the checkpoint, but the separate 5-point milestone rubric includes progress shown in Lab 3. Since the student expects to be away, request permission for **remote demonstration or a short alternative slot**; do not assume absence is excused automatically.

## Before showing the work

- [ ] Download/extract `CMPE411_SmartCart_Reviewed` and run **on your own Mac**.
- [ ] Install dependencies and run `python3 -m pytest -q` — the preparation run showed **65 passed**; capture your own terminal output.
- [ ] (Optional) Show `python3 -m pytest -q --cov=cart --cov=api --cov-branch --cov-report=term-missing`; preparation measured **98%**, not a guarantee on every setup.
- [ ] Review `docs/requirements.md` and `docs/TEST_REQUIREMENTS_MATRIX.md`; be ready to explain 500 TL BVA, discount decision table, validation limits and unit vs API.
- [ ] Commit and publish to a **new GitHub repository**, not to `cmpe411-lab1`. Verify `.venv` is not tracked.
- [ ] Send the repository link and request for remote progress review to the instructor before 20 November.
- [ ] Check Learn for any newer schedule or a separate upload slot.

## Five-minute demo sequence

1. Open repository root and `docs/requirements.md`.
2. Say the four main rules: subtotal, member 5%, SAVE10 10% at >=500 TL, no stacking.
3. Run `python3 -m pytest -q`; show the green suite and identify unit vs API files.
4. Point to 499.99/500.00/500.01 and NaN/Infinity, malformed item, large-quantity checks.
5. If asked, show `python3 tools/check_mutations.py` and explain the **selected set** of 9 mutants, not whole-program 100% mutation coverage.
6. Be honest: the **separate AI test candidate evaluation and final PDF are in progress**, not completed.

## Brief English explanation

> My project is a specification-driven shopping cart and discount engine. I test it at the unit and API levels, using boundary value analysis around the 500 TL coupon threshold and decision tables for membership and coupon combinations. I also check invalid input handling and use selected mutations to assess whether the suite notices faults. I am documenting an independent review of AI-generated candidates for the final report.
