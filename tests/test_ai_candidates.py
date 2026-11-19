"""Reviewed Option A candidates. See docs/ai-experiment/review.md for provenance."""

from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from api import app
from cart import CartValidationError, calculate_checkout


MONEY_FIELDS = ("subtotal", "discount_amount", "total")


def line(price, quantity=1):
    return {"unit_price": price, "quantity": quantity}


def assert_core_checkout(result, expected):
    subtotal, discount, total, label = expected
    assert isinstance(result, dict)
    for field, value in zip(MONEY_FIELDS, (subtotal, discount, total)):
        assert isinstance(result[field], Decimal)
        assert result[field] == Decimal(value)
    assert result["applied_discount"] == label


@pytest.mark.parametrize(
    "items, options, expected",
    [
        pytest.param(
            [line("500.05")],
            {"coupon": "SAVE10"},
            ("500.05", "50.01", "450.04", "SAVE10"),
            id="SC02-adapted-coupon-tie",
        ),
        pytest.param(
            [line("499.99")],
            {"is_member": True, "coupon": "SAVE10"},
            ("499.99", "25.00", "474.99", "member"),
            id="SC04",
        ),
    ],
)
def test_core_discount_rules(items, options, expected):
    result = calculate_checkout(items, **options)
    assert_core_checkout(result, expected)


def test_SC06_coupon_wins_with_reordered_or_split_lines():
    items = [line("250.00", 2), line("0.01")]
    split_items = [line("250.00"), line("250.00"), line("0.01")]
    for representation in (items, list(reversed(items)), split_items):
        result = calculate_checkout(
            representation, is_member=True, coupon="SAVE10"
        )
        assert_core_checkout(result, ("500.01", "50.00", "450.01", "SAVE10"))


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_SC07_api_accepts_json_number_and_string_prices(client):
    response = client.post(
        "/checkout",
        json={"items": [line(12.25, 2), line("0.50", 3), line(0)]},
    )
    assert response.status_code == 200
    payload = response.json()
    for field, expected in zip(MONEY_FIELDS, ("26.00", "0.00", "26.00")):
        assert isinstance(payload[field], str)
        assert Decimal(payload[field]) == Decimal(expected)
    assert payload["applied_discount"] == "none"


@pytest.mark.parametrize(
    "items",
    [
        pytest.param([line("1.00") for _ in range(101)], id="SC09"),
        pytest.param([line("-0.01")], id="SC11"),
        pytest.param([line("1000000.01")], id="SC14"),
        pytest.param([line("1.00", 10001)], id="SC17"),
    ],
)
def test_core_rejects_invalid_items(items):
    with pytest.raises(CartValidationError):
        calculate_checkout(items)
