# SmartCart v1.1 — CMPE 411 Term Project #35

A small Python shopping cart and discount calculation system. **The main objective is specification-based software testing, not a complete e-commerce website.**

## 1. Install and run (Python 3.11 or newer)

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pytest -q
```

Windows virtual environment activation: `.venv\Scripts\activate`.

Optional detailed coverage:

```bash
python3 -m pytest -q --cov=cart --cov=api --cov-branch --cov-report=term-missing
```

Optional reproducible *selected* mutation experiment (temporary copies only):

```bash
python3 tools/check_mutations.py
```

To launch an HTTP API interactively (not needed for automated tests):

```bash
uvicorn api:app --reload
```

Open `http://127.0.0.1:8000/docs` for FastAPI's interactive documentation. API tests use an in-process TestClient and do not require a running server.

## 2. Written rules

- Original subtotal = sum of unit prices x quantities, calculated with `Decimal`.
- Members receive 5%. The case-sensitive `SAVE10` coupon gives 10% on original subtotals at least 500.00 TL. Discounts **never stack**.
- Validate finite prices, product object shapes, quantities and coupons. Project-defined safety caps: price up to 1,000,000.00 TL, 10,000 units per line and 100 lines per cart.
- Money rounds to two decimals (discount using `ROUND_HALF_UP`).
- Invalid core inputs raise `CartValidationError`; invalid API requests return HTTP 422.

**Full specification / oracle:** `docs/requirements.md`. These are our own declared business rules, not mandated by the instructor.

## 3. Testing strategy

| Level | Tests | What is exercised? |
|---|---|---|
| Unit | `tests/test_cart_unit.py`, `tests/test_cart_edge_cases.py` | Discount logic, boundaries, negative values, rounding, metamorphic relations |
| API | `tests/test_checkout_api.py`, `tests/test_api_edge_cases.py` | HTTP status, JSON/schema validation, 4 response fields |

Black-box techniques include **equivalence partitioning, boundary value analysis and decision tables**. See `docs/TEST_REQUIREMENTS_MATRIX.md` for exact traceability, `docs/LAB3_DEMO_AND_ORAL_QA.md` for explanations, and `docs/CHANGELOG_REVIEW.md` for changes versus the starter.

## 4. Measured evidence and limits

See `docs/PROGRESS_REVIEWED_2026-11-13.md` for the dated, environment-specific evidence and `docs/SELECTED_MUTATION_RESULTS.md` for a deliberately small mutation sample. A high coverage percentage is **not** proof of correctness. Rerun everything on your own machine and after each change.

## 5. Course milestones

- **Lab 3 (originally Fri 20 Nov 2026):** show at least 10 running automated tests. See `docs/LAB3_CHECKLIST.md`.
- **Final (Fri 11 Dec 2026 23:59):** deliver GitHub link and **8–12 page PDF** in required report template, with at least 20 tests, two test levels, two test-design techniques and a validated AI testing element.

**AI evaluation is NOT finished.** Initial implementation, baseline tests and review improvements were drafted with AI assistance. The final project still needs an independently reviewed AI-test generation experiment, evidence of kept/fixed/rejected candidates and real baseline-versus-AI comparisons. See `docs/AI_EVALUATION_PLAN.md` and `docs/AI_USAGE_DRAFT.md`. Do not claim that AI-authored starter tests were manually authored.
