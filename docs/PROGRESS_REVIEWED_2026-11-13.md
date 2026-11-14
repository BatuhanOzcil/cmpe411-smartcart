# Verified progress — 13 November 2026, reviewed package

This document describes a **real run in the preparation environment** (Linux, Python 3.13.5, pytest 9.0.2, FastAPI 0.128.2). It does **not** claim the updated package has been run on the student's Mac or pushed to GitHub.

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

## Lab 3 / final status

- Original Lab 3 date: **Friday 20 November**. The brief requests at least **10 running tests**, in lab, marked as a progress check and not a standalone graded task, but progress is mentioned in the 5-point milestones rubric. Remote attendance/demonstration needs instructor approval.
- Final due **11 December 23:59**: repo link + 8–12-page PDF template report. The AI-generated test validation experiment, human confirmation and full report are not yet complete.

## Important provenance

Initial code/tests and review improvements were generated with AI assistance. These results are based on actual automated runs, but **human validation of test oracles and requirements by the student is still necessary**. Do not describe these as independently manually authored tests or as a completed AI comparative study.
