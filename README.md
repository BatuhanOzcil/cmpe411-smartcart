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

Run the supplemental mutation sample with `python3 tools/check_mutations.py --supplemental`.

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
| Unit and API | `tests/test_ai_candidates.py` | Eight reviewed Option A cases for discount interactions, rounding, boundaries, and JSON parsing |

Black-box techniques include **equivalence partitioning, boundary value analysis and decision tables**. See `docs/TEST_REQUIREMENTS_MATRIX.md` for exact traceability, `docs/LAB3_DEMO_AND_ORAL_QA.md` for explanations, and `docs/CHANGELOG_REVIEW.md` for changes versus the starter.

## 4. Measured evidence and limits

On Python 3.12.14 the combined suite passed **73 tests** (50 unit and 23 API). It covered 69/71 statements and 24/24 branches. The coverage tool displays 98% when it combines both counts. The suite killed all nine historical selected mutants and all three supplemental ones. These figures apply to the [measured groups and selected changes](docs/ai-experiment/results.md).

## 5. Option A experiment

An isolated ChatGPT generation from the written specification produced 18 candidates. Review kept seven, adapted one to check a coupon-rounding tie, and rejected ten that overlapped with existing checks. The baseline was already AI-assisted. The adapted case killed a coupon-only rounding mutant that survived both the baseline and the raw candidates.

- [Exact prompt](docs/ai-experiment/prompt.md) and [raw model response](docs/ai-experiment/raw_response.md)
- [Per-candidate review](docs/ai-experiment/review.md)
- [Coverage, mutation comparison, and reproduction commands](docs/ai-experiment/results.md)
