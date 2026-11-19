# Option A measurements

The application and frozen specification match commit `1d8be2f`. All groups ran on Python 3.12.14 with the same [package versions](environment.txt). A passed case means one pytest collection node. There were no failures, errors or skips on the unmodified application.

| Measure | AI-assisted baseline | Reviewed additions | Combined |
|---|---:|---:|---:|
| Passing tests (unit + API) | 65 (43 + 22) | 8 (7 + 1) | 73 (50 + 23) |
| Statement coverage | 69/71 (97.2%) | 63/71 (88.7%) | 69/71 (97.2%) |
| Branch coverage | 24/24 (100%) | 18/24 (75%) | 24/24 (100%) |
| Displayed combined coverage | 98% | 85% | 98% |
| Original selected mutants killed / survived / errors | 9 / 0 / 0 | 7 / 2 / 0 | 9 / 0 / 0 |
| Supplemental mutants killed / survived / errors | 2 / 1 / 0 | 3 / 0 / 0 | 3 / 0 / 0 |

Coverage.py computes the combined percentage from exercised statements and branches. For the baseline and union this is 93/95 (97.89%). In both, only the defensive exception handler in `api.py` (lines 46–47) was unexecuted. Invalid JSON requests normally fail schema validation before the handler. The candidate-only group intentionally covers selected behaviors.

| Mutant | Change | Baseline | Reviewed | Combined |
|---|---|---|---|---|
| M1 | Exclude exactly 500 TL | Killed | Survived | Killed |
| M2 | Membership becomes 6% | Killed | Killed | Killed |
| M3 | Coupon becomes 9% | Killed | Killed | Killed |
| M4 | Accept one extra unit | Killed | Killed | Killed |
| M5 | Accept one extra cent of unit price | Killed | Killed | Killed |
| M6 | Accept one extra cart line | Killed | Killed | Killed |
| M7 | Skip the core's unknown-coupon rejection | Killed | Survived | Killed |
| M8 | Ignore quantity in subtotal | Killed | Killed | Killed |
| M9 | Use half-even for every discount | Killed | Killed | Killed |
| M10 | Use half-even for coupon discounts only | Survived | Killed | Killed |
| M11 | Skip membership for an ineligible coupon | Killed | Killed | Killed |
| M12 | Default API requests to member | Killed | Killed | Killed |

The raw 18 candidates caught eight primary mutants and two supplemental ones. M7 and M10 survived. M10 was caught only after the review adapted SC02. The original checkpoint's 9/9 result provided no room for a higher score on those nine mutants. Both baseline and combined exercised the same lines and branches. The combined suite gained a specified input at which it detects an additional rounding regression. The supplemental sample was selected for specific behaviors and these proportions apply only to the selected mutants.

## Reproduce

Install from `requirements.txt` as described in the [README](../../README.md), or use `python -m pip install -r docs/ai-experiment/environment.txt` to match the experiment's dependencies. From the repository root with the environment active:

```bash
baseline=(tests/test_cart_unit.py tests/test_cart_edge_cases.py
          tests/test_checkout_api.py tests/test_api_edge_cases.py)
reviewed=(tests/test_ai_candidates.py)

python -m pytest -q "${baseline[@]}" --cov=cart --cov=api --cov-branch --cov-report=json
python -m pytest -q "${reviewed[@]}" --cov=cart --cov=api --cov-branch --cov-report=json
python -m pytest -q --cov=cart --cov=api --cov-branch --cov-report=json

python tools/check_mutations.py "${baseline[@]}"
python tools/check_mutations.py "${reviewed[@]}"
python tools/check_mutations.py
python tools/check_mutations.py --supplemental "${baseline[@]}"
python tools/check_mutations.py --supplemental "${reviewed[@]}"
python tools/check_mutations.py --supplemental
```

The coverage commands above are Bash commands and overwrite `coverage.json` between runs. Its `totals` section contains independent line and branch counts. To replay the raw response, extract its Python block verbatim into `tests/test_generated_raw.py` in a disposable checkout and select that file explicitly in both tools. [Measured output](measured-output.txt) includes the failing pytest nodes for each mutation. The Starlette test-client deprecation warning in the local dependency set did not affect the run outcomes.
