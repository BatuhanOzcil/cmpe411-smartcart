# Review changes — 13 November 2026

Relative to `CMPE411_SmartCart_Lab3_Starter.zip`:

1. **R2 finite prices:** Added specific tests for `NaN` and `Infinity` (including float representations). Existing core rejection is now a regression-tested behavior; Pydantic API rejects nonfinite price strings as HTTP 422.
2. **R1 item shape:** Added core tests for non-dictionary line items and HTTP tests for non-object JSON line items.
3. **Resource/number limits:** Explicitly documented `unit_price <= 1000000.00`, `quantity <= 10000`, `cart lines <= 100`. Added core/API validation and exact-upper-bound tests. Verified the maximum accepted cart total can be calculated without Decimal errors.
4. **Test-design quality:** Added metamorphic checks for item reordering and splitting identical item quantities, plus a requirements-to-tests map.
5. **Reproducible selected mutations:** Added `tools/check_mutations.py`, which runs deliberate changes in temporary copies, without modifying the original project.
6. **Reproducibility:** Added a GitHub Actions workflow and documented the checkpoint's installation, test, and AI usage details.

No accounts, database, payments, stock, checkout UI or unrelated functionality were added.

The [completed Option A experiment](ai-experiment/results.md) uses this reviewed suite as its AI-assisted baseline.
