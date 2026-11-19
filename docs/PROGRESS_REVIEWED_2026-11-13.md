# Verified progress — 13 November 2026, reviewed package

This historical checkpoint records a run in the preparation environment (Linux, Python 3.13.5, pytest 9.0.2, FastAPI 0.128.2). To reproduce the 65-test checkpoint, use the [frozen source revision](https://github.com/BatuhanOzcil/cmpe411-smartcart/tree/1d8be2f4eb1ce99439d24aafefd3d833ff145dfb).

## Reproducible commands

```bash
python3 -m pytest -q
python3 -m pytest -q --cov=cart --cov=api --cov-branch --cov-report=term-missing
python3 tools/check_mutations.py
```

## Observed results

- **65 passed** across direct Python unit tests and FastAPI TestClient API tests.
- Combined statement/branch coverage: **98%** (`cart.py`: 100%, `api.py`: 92%); two defensive exception-handling lines in `api.py` were not reached by these HTTP tests.
- A **selected sample of 9 source mutations** was run by a reproducible script, each on its own temporary copy of the project. **9 killed, 0 survived, 0 execution errors**, kill rate **100% of those 9 mutants**. This is **not** a whole-code mutation score and must not be presented as such.
- All newly added validation scenarios passed, including NaN/Infinity, malformed items, max quantity/price/cart lines, maximum supported cart, and two metamorphic relations.

## Rules and test levels

- Requirements/expected values: `docs/requirements.md`.
- Tests: Python core unit tests + FastAPI in-process HTTP tests.
- Techniques: decision table, equivalence partitioning, boundary value analysis and metamorphic relations.
- Chosen guardrails: max price 1,000,000 TL, 10,000 units per line, 100 cart lines (our policy, not an instructor requirement).

## Final evaluation

The initial code, tests, and review improvements used AI assistance. The [completed Option A experiment](ai-experiment/results.md) compares this baseline with the reviewed candidates and the combined suite.
