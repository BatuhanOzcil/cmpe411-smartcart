# Option A candidate review

On 19 November 2026 an isolated OpenAI ChatGPT generation session in Codex produced the first response in [raw_response.md](raw_response.md) from [prompt.md](prompt.md). It received the public interfaces and the written requirements at commit `1d8be2f4eb1ce99439d24aafefd3d833ff145dfb`. It was given neither the implementation nor the baseline or mutant selection and did not inspect them. The session used the inherited GPT-6-based Codex model with no sampling overrides. The exact backend revision and sampling values were unavailable. The raw response SHA-256 is `9348afb9504e90851f6ba0b2aadc945abe312c17d99c1fc58303c822d34b892f`.

The reviewer was Codex with access to the pinned specification, implementation, baseline and measurements. All 18 raw candidates executed and passed on unmodified code. Each had a falsifiable assertion and a defensible outcome. Review checked the import and API path, derived money and rejection outcomes from R1–R9, checked overlap by level and oracle, and measured sensitivity to code changes. No student-authored test group or student verification is claimed. The reviewed file retains seven candidate scenarios as supplied and one adapted scenario. Ten candidates were rejected from the combined suite. The two ambiguity notes are addressed below.

| Candidate | Decision | Requirement and review rationale | Failed raw mutants |
|---|---|---|---|
| SC01 | Reject | R1–R5, R8. The full legal cart and trillion-lira total are already exercised by `test_maximum_supported_cart_calculates_without_decimal_errors`. Checking the extra zero-discount field adds little to this workload case. | M8 |
| SC02 | Fix | R8. `0.10 × 5% = 0.005` correctly expects 0.01 and duplicates `test_round_half_up_on_member_discount`. Adapt to a coupon tie at 500.05 TL. The coupon discount is 50.005 before rounding, 50.01 after rounding, and the total is 450.04. The input and oracle adaptation came from the review. | M9 |
| SC03 | Reject | R6. `test_coupon_boundary[just_below_500]` already verifies the same no-discount policy and `test_checkout_success[coupon_below_limit]` checks the total at the API. | None |
| SC04 | Keep | R5–R8. At 499.99 the coupon is ineligible, but 5% is 24.9995, which rounds to 25.00. The existing fallback test exercises 200.00 TL. This case combines a near-threshold cart and an explicit full checkout oracle. | M2, M11 |
| SC05 | Reject | R6. The exact 500.00 TL input is already tested by two unit cases and the API. The candidate correctly killed the boundary mutant. | M1, M3 |
| SC06 | Keep | R4–R8. The three representations of 500.01 must all give 50.00 discount and 450.01 total. The baseline exercises reordering and splitting separately. This case combines both with membership competition, multi-line arithmetic and the upper neighbor. | M3, M8 |
| SC07 | Keep | R2, R4, R8–R9. Mixed JSON numbers and strings plus omitted flags exercise parsing and defaults. The literal subtotal is 12.25 × 2 + 0.50 × 3 + 0 = 26.00. Check the three money fields' types and values and the label. | M8, M12 |
| SC08 | Reject | R1, R9. Same empty-list input and exception as `test_empty_cart_is_rejected`. | None |
| SC09 | Keep | R1, R9. The fixed value 101 protects the written limit independently. The baseline constructs the input with `MAX_CART_ITEMS + 1`. | M6 |
| SC10 | Reject | R1, R9. Same wrong item type as API `string_item`; the text itself is immaterial. | None |
| SC11 | Keep | R2, R9. Adds the immediate invalid neighbor −0.01 below the allowed 0.00. The baseline's representative negative price is −1.00. | None |
| SC12 | Reject | R2, R9. Same NaN string and core exception as baseline `nan_text`. | None |
| SC13 | Reject | R2, R9. Same API extra-fraction partition as `too_many_cents`. Both have a nonzero third place and expect 422. | None |
| SC14 | Keep | R2, R9. The fixed 1,000,000.01 TL input checks the written core limit even if the implementation constant changes. The HTTP baseline separately uses a literal. | M5 |
| SC15 | Reject | R3, R9. Same zero-quantity core exception as baseline. | None |
| SC16 | Reject | R3, R9. Same bool-versus-integer HTTP case already covered by `boolean_quantity`. | None |
| SC17 | Keep | R3, R9. The literal 10,001 checks the exact core boundary independently of `MAX_QUANTITY`. | M4 |
| SC18 | Reject | R6, R9. Existing API `wrong_case_coupon` already expects 422; membership should not change schema validity. This candidate did not catch core M7 because Pydantic rejected the request before the core ran. | None |

“None” means no failure was observed in these 12 selected mutations. It says nothing about whether a test could detect other changes. SC06 checks three representations within one collected case. Candidate IDs are retained in `tests/test_ai_candidates.py`.

## Ambiguities and omissions

- **Money format.** R8 lists three monetary values and one label. R9's reference to “four monetary fields” means all four response fields with only the three money values encoded as strings. The review kept SC07's string type plus exact Decimal value checks. A fixed number of trailing zeroes is an implementation behavior already captured by the baseline's exact JSON case.
- **Quantity coercion.** The response suggested that string `"1"` and JSON number `1.0` might be open to interpretation. R1 rejects wrong types, R3 specifies an integer, and R2 explicitly allows strings for price. The strict API interpretation therefore requires integer-typed quantities. Separate exploratory requests confirmed both received 422. This clarification did not change any candidate oracle.
- **Missing cases.** The raw suite's only invalid-coupon test is at the API level and does not check direct core rejection. M7 survived. The raw suite also misses the coupon-specific half-cent case, so M10 survived. An exact-threshold case was generated and killed M1. It was deliberately removed from the reviewed additions because the baseline already covers it.

See [results.md](results.md) for measured comparisons and commands. See [protocol.md](protocol.md) for the frozen code and supplemental mutation selection.
