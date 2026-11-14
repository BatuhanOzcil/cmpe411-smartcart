# Historical starter snapshot (before quality review): Progress snapshot — 13 November 2026

The first version was executed and verified in the preparation environment. These figures are **real local results**, not proof that they have already been reproduced on the student's Mac or uploaded to GitHub.

- `python -m pytest -q`: **38 passed**.
- `python -m pytest -q --cov=cart --cov=api --cov-branch --cov-report=term-missing`: **38 passed**, **96% total coverage** in this environment (cart.py 97%, api.py 92%). These percentages are baseline measurement, not a comparison with separately accepted LLM tests.
- Test levels: **unit tests** for calculation rules and **API tests** using FastAPI TestClient.
- Test techniques: **decision table**, **equivalence partitioning**, **boundary value analysis** (499.99 / 500.00 / 500.01).
- Project checkpoint: at least 10 running tests on **20 Nov**, original published schedule. This code exceeds that number in the preparation environment.

## Still not done

- Run and verify on the student's own Mac, then push to a new GitHub repository.
- Perform **independent** LLM test-generation, preserve prompts and candidates, document keep/fix/reject decisions, compare tests using real mutation outcomes.
- Final report according to the instructor's report template, PDF 8–12 pages, due **11 Dec 23:59**.
- Confirm any updated dates or Lab 2 make-up announcements on Learn.

## Authorship and evaluation honesty

Starter code and tests were prepared with AI assistance. Human review by the student is required; do not claim tests were independently authored or AI validation completed. Project focus is correctness and critical testing analysis, not just the number of passing tests.
