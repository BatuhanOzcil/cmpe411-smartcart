# Historical starter snapshot (before quality review): Progress snapshot — 13 November 2026

The first version was executed and verified in the preparation environment. These figures are **real local results**, not proof that they have already been reproduced on the student's Mac or uploaded to GitHub.

- `python -m pytest -q`: **38 passed**.
- `python -m pytest -q --cov=cart --cov=api --cov-branch --cov-report=term-missing`: **38 passed**, **96% total coverage** in this environment (cart.py 97%, api.py 92%). These percentages are baseline measurement, not a comparison with separately accepted LLM tests.
- Test levels: **unit tests** for calculation rules and **API tests** using FastAPI TestClient.
- Test techniques: **decision table**, **equivalence partitioning**, **boundary value analysis** (499.99 / 500.00 / 500.01).
- Project checkpoint: at least 10 running tests on **20 Nov**, original published schedule. This code exceeds that number in the preparation environment.

## Work that followed this snapshot

The [13 November reviewed package](PROGRESS_REVIEWED_2026-11-13.md) expanded the suite to 65 passing tests. The [completed Option A experiment](ai-experiment/results.md) records the isolated generation run and the final comparison with 73 passing tests in the combined suite.

## Authorship and evaluation honesty

The starter code and tests were prepared with AI assistance. The results on this page describe the starter snapshot only.
