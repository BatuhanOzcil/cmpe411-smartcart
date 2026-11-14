"""Unit tests: direct calls to the business rules, not the HTTP API."""

from decimal import Decimal

import pytest

from cart import CartValidationError, calculate_checkout


def item(price, quantity=1):
    return {"unit_price": price, "quantity": quantity}


@pytest.mark.parametrize(
    "items,member,coupon,subtotal,discount,total,applied",
    [
        ([item("100.00")], False, None, "100.00", "0.00", "100.00", "none"),
        ([item("100.00", 2)], True, None, "200.00", "10.00", "190.00", "member"),
        ([item("500.00")], False, "SAVE10", "500.00", "50.00", "450.00", "SAVE10"),
        ([item("500.00")], True, "SAVE10", "500.00", "50.00", "450.00", "SAVE10"),
        ([item("200.00")], True, "SAVE10", "200.00", "10.00", "190.00", "member"),
        ([item("100.00")], False, "SAVE10", "100.00", "0.00", "100.00", "none"),
        ([item("100.00", 2), item("150.00", 2)], False, "SAVE10", "500.00", "50.00", "450.00", "SAVE10"),
        ([item("0.00")], False, None, "0.00", "0.00", "0.00", "none"),
    ],
    ids=[
        "regular_no_discount", "member_five_percent", "coupon_ten_percent",
        "member_and_coupon_no_stacking", "member_under_threshold",
        "coupon_under_threshold_no_member", "multiple_items_coupon", "zero_price_allowed",
    ],
)
def test_decision_table(items, member, coupon, subtotal, discount, total, applied):
    result = calculate_checkout(items, is_member=member, coupon=coupon)
    assert result["subtotal"] == Decimal(subtotal)
    assert result["discount_amount"] == Decimal(discount)
    assert result["total"] == Decimal(total)
    assert result["applied_discount"] == applied


@pytest.mark.parametrize(
    "price,applied,expected_discount",
    [
        ("499.99", "none", "0.00"),
        ("500.00", "SAVE10", "50.00"),
        ("500.01", "SAVE10", "50.00"),
    ],
    ids=["just_below_500", "exactly_500", "just_above_500"],
)
def test_coupon_boundary(price, applied, expected_discount):
    result = calculate_checkout([item(price)], coupon="SAVE10")
    assert result["applied_discount"] == applied
    assert result["discount_amount"] == Decimal(expected_discount)


@pytest.mark.parametrize("bad_price", ["-1.00", "1.234", "not-a-number", True])
def test_invalid_price_is_rejected(bad_price):
    with pytest.raises(CartValidationError):
        calculate_checkout([item(bad_price)])


@pytest.mark.parametrize("bad_quantity", [0, -1, 1.5, True])
def test_invalid_quantity_is_rejected(bad_quantity):
    with pytest.raises(CartValidationError):
        calculate_checkout([item("10.00", bad_quantity)])


@pytest.mark.parametrize("bad_coupon", ["SAVE20", "save10"])
def test_unknown_or_wrong_case_coupon_is_rejected(bad_coupon):
    with pytest.raises(CartValidationError):
        calculate_checkout([item("600.00")], coupon=bad_coupon)


def test_empty_cart_is_rejected():
    with pytest.raises(CartValidationError):
        calculate_checkout([])


def test_membership_must_be_boolean():
    with pytest.raises(CartValidationError):
        calculate_checkout([item("100.00")], is_member="yes")


def test_round_half_up_on_member_discount():
    result = calculate_checkout([item("0.10")], is_member=True)
    assert result["discount_amount"] == Decimal("0.01")
    assert result["total"] == Decimal("0.09")
