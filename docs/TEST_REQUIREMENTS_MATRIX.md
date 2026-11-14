# What the tests mean — traceability matrix

The relevant distinction is not "64 tests is better than 20". Each group checks an identified risk or requirement.

| Requirement / risk | Test files and examples | Technique and oracle |
|---|---|---|
| R5/R6/R7 membership, coupon, no stacking | `test_cart_unit.py::test_decision_table` | Decision table; written requirements |
| R6 coupon 500 TL threshold | `test_cart_unit.py::test_coupon_boundary` | Boundary values 499.99 / 500 / 500.01 |
| R2 invalid prices | `test_cart_unit.py::test_invalid_price_is_rejected` and `test_cart_edge_cases.py::test_nonfinite_unit_price_rejected` | Equivalence partitioning; specified invalid-input behavior |
| R1 invalid items/cart size | `test_cart_edge_cases.py::test_product_must_be_object`, `test_too_many_items_rejected`, `test_maximum_number_of_items_is_valid` | Invalid partitions; 100/101 line count boundary |
| R3 quantity type and limits | `test_cart_unit.py::test_invalid_quantity_is_rejected`, `test_cart_edge_cases.py::test_excessive_quantities_rejected_cleanly`, `test_maximum_quantity_is_valid` | Invalid partitions; 0/1 and 10,000/10,001 boundaries |
| R2 price upper bound | `test_cart_edge_cases.py::test_price_at_maximum_allowed`, `test_price_above_maximum_is_rejected` | Boundary at 1,000,000.00 TL |
| R4/R8 arithmetic and rounding | `test_cart_unit.py::test_round_half_up_on_member_discount`, `test_maximum_supported_cart_calculates_without_decimal_errors` | Specified expected values and boundary checks |
| R4 item/order consistency | `test_cart_edge_cases.py::test_permuting_line_items_does_not_change_result`, `test_splitting_a_line_item_preserves_total` | Metamorphic relations |
| R9 HTTP contract and validation | `test_checkout_api.py`, `test_api_edge_cases.py` | API-level contract: 200, 422 and exact money fields |

## Why repeat some cases across unit and API?

Unit tests show the *calculation* is correct. API tests show the same rules survive *JSON parsing, schema validation, routing and serialization*. They test different risks, not just copies of a test.

## What coverage does NOT prove

After the review, coverage is measured separately for `cart.py` and `api.py`. The API's defensive catch for `CartValidationError` can remain uncovered because normal invalid HTTP data is rejected earlier by Pydantic. We do not add artificial tests solely to claim 100%. Coverage says what ran; mutation testing helps show if tests notice meaningful changes.
