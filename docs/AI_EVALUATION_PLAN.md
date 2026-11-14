# AI test validation plan — upcoming work (NOT completed yet)

## Official expectation

Project brief #35 suggests **Option A: LLM-generated decision-table tests, validated**. A strong final submission shows the actual prompts, test candidates accepted/fixed/rejected and why, and a careful empirical comparison using coverage and mutation results.

**Honesty:** Both the original 38 tests and the added edge-case tests were drafted with AI assistance. The 13 November run of **65 passing tests, 98% combined coverage and 9/9 selected mutant kills** is a real verified *current-suite* result, but is **not** yet evidence of an independently human-written baseline-versus-AI experiment. These distinctions must be kept in the report.

## Reproducible future procedure

1. Freeze `docs/requirements.md` before asking for candidate tests. Independently confirm the specification and decision table.
2. Record the exact model name, date, prompt and unedited AI candidate tests in `docs/AI_TEST_REVIEW_LOG.md` (create this when the experiment actually runs).
3. Give the **specification** and `calculate_checkout` public interface, not observed output from the buggy implementation.
4. For every AI-generated candidate, mark **Keep / Fix / Reject / Ask**, state the specific requirement and reasoning, identify invented APIs, copied bugs, unsupported assumptions, duplicates, missing boundaries and weak assertions.
5. Validate expected outputs directly against the frozen specification. Run tests repeatedly, compare actual coverage on agreed baselines, and document the exact test groups used.
6. Test select mutants on **both** groups in separate copies (example: `>= 500` becomes `> 500`). Document killed/surviving and reasons. Do not count equivalent mutants as test-suite failures.
7. Produce a short critical analysis: where AI improved tests, where it generated invalid or redundant cases, cost of human review, and limitations. Include this in the required final PDF report.
8. Have the student inspect and explain every submitted test; never invent errors, human reviews or experimental scores.

## A five-part RCTOC prompt template (NOT yet run as a separate recorded experiment)

> **Role:** You are a software tester.  
> **Context:** Use the written SmartCart specification below, and only the public function `calculate_checkout(items, is_member=False, coupon=None)` in `cart.py`.  
> **Technique:** Use equivalence partitioning, boundary value analysis and decision tables.  
> **Output format:** First propose a compact test table with input, expected output and requirement ID. After confirmation, write pytest `parametrize` tests.  
> **Constraints:** Expected outputs must come only from the specification, not from running the code. Do not invent functions, coupons, fields, expiry rules or price caps other than those in the spec. List ambiguity instead of guessing.

Paste the **current** `docs/requirements.md` after this prompt when actually running the experiment. Save the response *verbatim* before modifying it.
