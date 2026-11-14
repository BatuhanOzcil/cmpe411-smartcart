# Lab 3 / possible oral questions — short, explainable English answers

**Use this as a study aid, not a script to read without understanding.** The official brief permits AI assistance but says you must explain every submitted part.

## Two-minute explanation

> My project is #35, a small Python shopping cart and discount engine. It calculates a subtotal, then applies only the highest eligible discount: 5% for members or 10% with SAVE10 when the original subtotal is at least 500 TL. My written specification is the test oracle. I use pytest unit tests to check the calculation and FastAPI TestClient API tests to check HTTP validation and response values. I applied decision tables for coupon/member combinations and boundary value analysis at 499.99, 500.00 and 500.01. I also added negative tests for nonfinite prices, malformed items and excessive quantities. I can demonstrate automated tests using `python3 -m pytest -q`.

## Likely questions and answers

**Q1: Why was this topic chosen?**
> It has clear business rules, measurable expected outputs and many useful boundary and decision-table test cases without requiring a large website.

**Q2: What is the specification / test oracle?**
> `docs/requirements.md` defines the expected results. Tests must use these rules rather than trust the existing code.

**Q3: Why 500 TL boundary values?**
> SAVE10 requires at least 500 TL. At 499.99 it does not apply, at 500.00 it does, and at 500.01 it still does. A `>` versus `>=` defect would be caught by exactly 500.00.

**Q4: What is the difference between unit and API tests?**
> Unit tests call `calculate_checkout` directly. API tests send JSON requests to `/checkout` and check status codes, schema validation and serialized results.

**Q5: What is your decision table?**
> It combines membership, presence of the known coupon and whether subtotal is at least 500 TL. It verifies no discount stacking and member discount below the coupon threshold.

**Q6: What if member and coupon are both valid?**
> Apply SAVE10 (10%) only; do not combine 10% and 5%.

**Q7: What if the coupon is invalid or lowercase?**
> Only the case-sensitive code SAVE10 is accepted. Unknown coupon codes raise an error in the core and cause HTTP 422 through the API.

**Q8: Why use Decimal and ROUND_HALF_UP?**
> Decimal avoids binary floating-point inaccuracies in money calculations. A 0.005 TL discount rounds to 0.01 TL with ROUND_HALF_UP.

**Q9: Why reject NaN, Infinity, wrong item types and giant numbers?**
> They are outside our written input domain; accepting them could create meaningless or unreliable totals. We defined explicit price, quantity and cart-size caps, and tested both valid upper limits and values just above them.

**Q10: Why are there more than the required 10 tests?**
> Ten is the Lab 3 checkpoint minimum, while the final brief requires at least twenty. Different tests cover distinct business rules, invalid partitions, boundaries and API behavior; quality matters more than the count.

**Q11: Is 98% coverage proof that the program is correct?**
> No. Coverage shows which statements and branches executed, not whether the expected values were correct. A weak assertion can still contribute to coverage.

**Q12: What is mutation testing?**
> We make small changes to code and run tests. A mutant is killed if tests fail. We ran a small reproducible set of selected mutations on temporary copies, not a full mutation analysis of every possible code change.

**Q13: What is an equivalent mutant?**
> A change that does not alter observable behavior. No test can kill an equivalent mutant, and it must be considered when interpreting mutation scores.

**Q14: What is a metamorphic relation here?**
> Changing the order of cart items, or splitting an identical item quantity into two lines, should not change the checkout total or applied discount.

**Q15: Why does the API return 422?**
> Invalid JSON payloads fail Pydantic validation. 200 means a valid checkout request and includes the four expected fields.

**Q16: What did AI do, and what remains to be validated?**
> AI tools assisted in drafting the code and candidate tests. I still need to review separately generated test candidates, document which ones I accept/reject, verify expected values against requirements and report honest comparison results. Do not claim this evaluation is complete until actually performed.

**Q17: What is the critical distinction between Lab 1, Lab 2 and this project?**
> Lab 1: a 2-kg boundary catches `< 2` instead of `<= 2`. Lab 2: a 64-character password boundary catches `>=64` instead of `>64`, then reviews AI tests. SmartCart: 500 TL coupon threshold, decision table, two test levels and documented validation.

**Q18: The instructor says 'show the tests'. What should you run?**
> `python3 -m pytest -q`, then `python3 -m pytest -q --cov=cart --cov=api --cov-branch --cov-report=term-missing`. For selected mutations, run `python3 tools/check_mutations.py`.

## Before claiming the final report is done

- Independently review all AI-assisted work yourself, preserving concrete examples and limitations.
- Perform the planned *AI-generated test* candidate review (prompts, kept/fixed/rejected tests and why).
- Compare the baseline suite to accepted AI tests with real coverage and mutation evidence.
- Write the actual 8–12-page PDF report using the instructor's template. The starter package does not contain that finished report.

**Q19: Why did the Mac previously show a StarletteDeprecationWarning?**
> A dependency warns that part of its TestClient API may change in a future release. It is not a failed test; the automated suite still needs to be rerun after dependency upgrades.
