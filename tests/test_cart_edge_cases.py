"""Additional targeted tests from the 13 Nov quality review.

Designed to close specific validation gaps, NOT simply inflate the test count.
"""

from decimal import Decimal

import pytest

from cart import (
    CartValidationError,
    MAX_CART_ITEMS,
    MAX_QUANTITY,
    MAX_UNIT_PRICE,
    calculate_checkout,
)


def item(price="10.00", quantity=1):
    return {"unit_price": price, "quantity": quantity}


@pytest.mark.parametrize(
    "nonfinite",
    ["NaN", "Infinity", "-Infinity", float("nan"), float("inf")],
    ids=["nan_text", "plus_infinity_text", "minus_infinity", "nan_float", "infinity_float"],
)
def test_nonfinite_unit_price_rejected(nonfinite):
    with pytest.raises(CartValidationError):
        calculate_checkout([item(nonfinite)])


@pytest.mark.parametrize("bad_item", [None, "product", 42, ["10.00", 1]])
def test_product_must_be_object(bad_item):
    with pytest.raises(CartValidationError, match="Each item must be an object"):
        calculate_checkout([bad_item])


@pytest.mark.parametrize("too_large_qty", [MAX_QUANTITY + 1, 10**100])
def test_excessive_quantities_rejected_cleanly(too_large_qty):
    with pytest.raises(CartValidationError, match="Quantity"):
        calculate_checkout([item(quantity=too_large_qty)])


def test_maximum_quantity_is_valid():
    result = calculate_checkout([item("1.00", MAX_QUANTITY)])
    assert result["subtotal"] == Decimal(MAX_QUANTITY)
    assert result["total"] == Decimal(MAX_QUANTITY)


def test_price_at_maximum_allowed():
    result = calculate_checkout([item(str(MAX_UNIT_PRICE))])
    assert result["subtotal"] == MAX_UNIT_PRICE


def test_price_above_maximum_is_rejected():
    with pytest.raises(CartValidationError, match="Price"):
        calculate_checkout([item(str(MAX_UNIT_PRICE + Decimal("0.01")))])


def test_too_many_items_rejected():
    with pytest.raises(CartValidationError, match="between 1 and"):
        calculate_checkout([item() for _ in range(MAX_CART_ITEMS + 1)])


def test_maximum_number_of_items_is_valid():
    result = calculate_checkout([item("1.00") for _ in range(MAX_CART_ITEMS)])
    assert result["subtotal"] == Decimal(MAX_CART_ITEMS)


def test_permuting_line_items_does_not_change_result():
    """Metamorphic relation: order of items cannot affect a money total."""
    items = [item("120.00", 2), item("260.00", 1), item("0.10", 3)]
    assert calculate_checkout(items, True, "SAVE10") == calculate_checkout(
        list(reversed(items)), True, "SAVE10"
    )


def test_splitting_a_line_item_preserves_total():
    """Metamorphic relation: splitting a quantity into two lines preserves totals."""
    original = calculate_checkout([item("100.00", 5)], coupon="SAVE10")
    split = calculate_checkout(
        [item("100.00", 2), item("100.00", 3)], coupon="SAVE10"
    )
    assert original == split


def test_maximum_supported_cart_calculates_without_decimal_errors():
    """100 lines x 10,000 units x 1,000,000 TL must remain deterministic."""
    result = calculate_checkout(
        [item(str(MAX_UNIT_PRICE), MAX_QUANTITY) for _ in range(MAX_CART_ITEMS)]
    )
    assert result["subtotal"] == Decimal("1000000000000.00")
    assert result["total"] == Decimal("1000000000000.00")
    assert result["applied_discount"] == "none"
