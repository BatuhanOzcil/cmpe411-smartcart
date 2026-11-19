# Role

You are a software tester preparing an independent set of candidate tests for SmartCart, a small Python shopping cart and discount engine.

# Context

Use only the written specification appended below and these public interfaces. The checkout function and exception are imported using `from cart import CartValidationError, calculate_checkout`. The unit interface returns a dict with Decimal money values and a string discount label. The API application is imported with `from api import app`. Use FastAPI's TestClient for `POST /checkout`; the top-level JSON object has `items`, optional `is_member` and optional `coupon`. API money values are strings. There is no existing suite or implementation in the material provided to you.

# Technique

Use a decision table for all valid membership/coupon rules, boundary value analysis around 500.00 TL, and equivalence partitioning for invalid inputs. Include a few cases that stress how the rules interact. Include some API-level cases where the transport contract matters.

# Output format

Return a compact table of 14 to 18 candidate cases with unique IDs, inputs, explicit expected outcomes, and requirement IDs. Then provide one complete pytest file in a single Python code block. Map the IDs to pytest test names or explicit parameter IDs. Add a short ambiguity note for behavior the specification leaves open.

# Constraints

Derive every expected outcome from the specification. Use literal expected values rather than implementing another discount calculator. Assert all four fields when testing a successful checkout, and the specified exception type or HTTP status for invalid data. Do not inspect, run, or infer expected results from any implementation or existing test suite. Do not invent interfaces, error message requirements, or business rules. If an ambiguity affects an oracle, flag it.

# SmartCart v1.1 — written specification / test oracle

This is the specification for **our own** CMPE 411 project #35. These are **project-defined rules**, not values mandated by the course instructor. Tests must derive expected results from these rules, not from the implementation. The 13 Nov quality review added explicit limits to prevent unrealistic requests from overflowing monetary calculations.

## Business rules

- **R1 Valid cart:** `items` is a list of 1 to **100** product line items, inclusive. Each item must be an object (Python dictionary / JSON object) containing `unit_price` and `quantity`. Missing fields or wrong types are invalid.
- **R2 Price:** Each unit price is a **finite**, nonnegative monetary amount from **0.00 to 1,000,000.00 TL** inclusive, with at most two meaningful decimal places. Zero-priced items are allowed; negative prices, `NaN`, `Infinity`, values above the maximum and extra fractions of a kuruş are rejected. Python core accepts ordinary finite numbers or numeric strings; the API uses JSON numbers or strings validated as Decimal.
- **R3 Quantity:** Each quantity is a **positive integer from 1 to 10,000** inclusive. Zero, negative, fractional, boolean, excessively large or missing quantities are rejected.
- **R4 Subtotal:** Sum `unit_price * quantity` across all line items using Python `Decimal`. Item order does not matter. Splitting the same item quantity between lines does not change totals.
- **R5 Membership:** An `is_member: bool` flag earns **5%** of the original subtotal; it is **not a login/account system**.
- **R6 Coupon:** The **only** coupon is case-sensitive `SAVE10`. It earns **10%** of the original subtotal when subtotal is **at least 500.00 TL**. A recognized coupon below threshold applies no coupon discount; an unknown/misspelled coupon is invalid. No expiry date and no discount cap exist.
- **R7 Discounts do not stack:** Apply one eligible discount only. SAVE10 (10%) wins over the member rate (5%) when eligible. Below 500 TL, a member receives 5% even if SAVE10 was provided but is ineligible.
- **R8 Money rounding:** Round the discount once to two decimals using `ROUND_HALF_UP`; compute `total = subtotal - discount`. Return `subtotal`, `discount_amount`, `total` and `applied_discount` (`none`, `member` or `SAVE10`).
- **R9 Errors and API contract:** The core `calculate_checkout(items, is_member=False, coupon=None)` raises `CartValidationError` for invalid cart data. The API's `POST /checkout` accepts JSON and returns HTTP **200** with all four monetary fields (Decimal values serialized as strings), or HTTP **422** for invalid inputs.

The item, price and quantity caps are **explicit safety policies we chose**, not special business requirements given by the lecturer. They make the input domain finite and keep worst-case arithmetic within a safe range (100 lines x 10,000 units x 1,000,000 TL = 1,000,000,000,000 TL). Real production systems would agree such limits with stakeholders.

## Decision table — only the known, correctly spelled coupon

| Member? | SAVE10 present? | Original subtotal >= 500? | Chosen discount |
|---|---|---|---|
| No | No | Any | none |
| Yes | No | Any | member: 5% |
| No | Yes | No | none |
| Yes | Yes | No | member: 5% |
| No | Yes | Yes | SAVE10: 10% |
| Yes | Yes | Yes | SAVE10: 10% |

Invalid coupons, malformed input and empty carts are separate negative equivalence partitions, **not** entries in this valid-data discount table.

## Test design / known oracles

- **Equivalence partitions:** valid / negative / nonfinite / too-precise / over-limit price; valid / zero / negative / fractional / boolean / over-limit quantity; dictionary / non-dictionary item; empty / valid / oversized cart; member / non-member; coupon absent / valid and eligible / valid but ineligible / invalid.
- **Boundary value analysis:** `499.99, 500.00, 500.01 TL` around the SAVE10 threshold; quantities `0, 1, 10,000, 10,001`; prices `0.00, 1,000,000.00, 1,000,000.01`; cart sizes `0, 1, 100, 101`.
- **Decision table:** combinations of membership, coupon presence and subtotal threshold.
- **Metamorphic relations:** reordering items or splitting a line item preserves the checkout result (for identical prices and quantities).
- **Test levels:** unit (direct calculation) and API (HTTP request, JSON validation, response contract).
- **Specified oracle:** this document establishes correct outputs. The fact that pytest returns PASS does not itself establish that these rules are correct or satisfy users.

## Intentionally out of scope

No payment processing, stock management, database, user accounts, coupon expiries, other coupon codes or UI. This keeps the course project centered on **testing**, not building a full e-commerce product.
