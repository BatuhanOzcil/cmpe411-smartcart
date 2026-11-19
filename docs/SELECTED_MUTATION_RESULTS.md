# Selected mutation test experiment — 13 November 2026

Historical 65-test checkpoint. Run `python3 tools/check_mutations.py` from the project root at the [frozen source revision](https://github.com/BatuhanOzcil/cmpe411-smartcart/tree/1d8be2f4eb1ce99439d24aafefd3d833ff145dfb) to reproduce this run. The script applies each of the nine selected changes in a separate temporary copy.

| Mutant | Source change | Result | Why useful? |
|---|---|---|---|
| M1 | `subtotal >= 500` → `> 500` | Killed | Exactly 500 TL boundary |
| M2 | Membership 5% → 6% | Killed | Rate correctness |
| M3 | Coupon 10% → 9% | Killed | Rate correctness |
| M4 | Allow quantity 10,001 | Killed | Maximum quantity guard |
| M5 | Allow unit price 1,000,000.01 | Killed | Maximum price guard |
| M6 | Allow 101 cart lines | Killed | Maximum cart size guard |
| M7 | Disable unknown-coupon rejection | Killed | Invalid coupon partition |
| M8 | Calculate subtotal without multiplying quantity | Killed | Multi-quantity money arithmetic |
| M9 | Use half-even instead of half-up rounding | Killed | Rounding at 0.005 TL |

**Measured outcome:** 9 selected mutants, 9 killed, 0 survived, 0 errors (**9/9 = 100% on the selected sample only**). See `tools/check_mutations.py` to reproduce the comparison exactly.

**Limitations:** These nine mutations were chosen deliberately, mostly to target existing high-value tests. No claim is made that all possible mutants are killed or that full code mutation coverage is 100%. Some mutants can be *equivalent* and impossible to distinguish; those need separate analysis. Full source-wide mutation analysis is not included in this checkpoint.

The [completed Option A comparison](ai-experiment/results.md) reports these nine selected changes and three supplemental changes for the AI-assisted baseline, reviewed additions, and combined suite.
