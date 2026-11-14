"""API-level checks exercise HTTP routing, parsing, schema and business logic."""

import pytest
from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


def payload(price="100.00", quantity=1, is_member=False, coupon=None):
    return {
        "items": [{"unit_price": price, "quantity": quantity}],
        "is_member": is_member,
        "coupon": coupon,
    }


@pytest.mark.parametrize(
    "data,expected_total,applied",
    [
        (payload("100.00"), "100.00", "none"),
        (payload("200.00", is_member=True), "190.00", "member"),
        (payload("500.00", coupon="SAVE10"), "450.00", "SAVE10"),
        (payload("500.00", is_member=True, coupon="SAVE10"), "450.00", "SAVE10"),
        (payload("499.99", coupon="SAVE10"), "499.99", "none"),
    ],
    ids=["regular_checkout", "member_checkout", "coupon_at_limit", "coupon_beats_member", "coupon_below_limit"],
)
def test_checkout_success(data, expected_total, applied):
    response = client.post("/checkout", json=data)
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == expected_total
    assert body["applied_discount"] == applied


@pytest.mark.parametrize(
    "data",
    [
        payload("-2.00"),
        payload("10.00", quantity=0),
        payload("10.00", quantity=-1),
        payload("10.123"),
        payload("600.00", coupon="WRONG"),
        payload("600.00", coupon="save10"),
        {"items": [], "is_member": False, "coupon": None},
        payload("10.00", quantity=True),
    ],
    ids=["negative_price", "zero_quantity", "negative_quantity", "too_many_cents",
         "unknown_coupon", "wrong_case_coupon", "empty_cart", "boolean_quantity"],
)
def test_checkout_rejects_invalid_payload(data):
    response = client.post("/checkout", json=data)
    assert response.status_code == 422


def test_checkout_full_money_fields_are_strings():
    response = client.post("/checkout", json=payload("500.00", coupon="SAVE10"))
    assert response.status_code == 200
    assert response.json() == {
        "subtotal": "500.00", "discount_amount": "50.00",
        "total": "450.00", "applied_discount": "SAVE10",
    }
