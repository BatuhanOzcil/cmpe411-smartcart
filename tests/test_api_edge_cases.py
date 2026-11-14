"""API-level edge cases: schema validation and HTTP behavior (not just core calls)."""

import pytest
from fastapi.testclient import TestClient

from api import app
from cart import MAX_CART_ITEMS, MAX_QUANTITY, MAX_UNIT_PRICE

client = TestClient(app)


def payload(price="10.00", quantity=1):
    return {"items": [{"unit_price": price, "quantity": quantity}]}


@pytest.mark.parametrize(
    "bad_payload",
    [
        payload("NaN"),
        payload("Infinity"),
        {"items": ["not-an-object"]},
        {"items": [None]},
        payload(quantity=MAX_QUANTITY + 1),
        payload(price="1000000.01"),
        {"items": [payload()["items"][0]] * (MAX_CART_ITEMS + 1)},
    ],
    ids=[
        "nan_price", "infinity_price", "string_item", "null_item",
        "quantity_above_limit", "price_above_limit", "too_many_items",
    ],
)
def test_api_rejects_new_invalid_cases(bad_payload):
    response = client.post("/checkout", json=bad_payload)
    assert response.status_code == 422
    assert response.json()["detail"]  # visible validation detail, not silent failure


def test_api_accepts_exact_quantity_and_price_limits():
    response = client.post(
        "/checkout",
        json=payload(str(MAX_UNIT_PRICE), MAX_QUANTITY),
    )
    assert response.status_code == 200
    body = response.json()
    assert body["subtotal"] == "10000000000.00"
    assert body["total"] == "10000000000.00"
    assert body["applied_discount"] == "none"
