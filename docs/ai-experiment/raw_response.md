## Candidate cases

A line is written as `(unit_price, quantity)`. Successful outcomes are listed in the order `subtotal, discount_amount, total, applied_discount`. Prices are numeric strings unless a JSON number is shown explicitly. The core defaults are nonmember and no coupon.

| ID | Level | Input | Expected outcome | Requirements |
|---|---|---|---|---|
| SC01 | Core | 100 lines of `(1000000.00, 10000)` | `1000000000000.00, 0.00, 1000000000000.00, none` | R1–R5, R8 |
| SC02 | Core | `(0.10, 1)`, member, no coupon | `0.10, 0.01, 0.09, member` | R3–R5, R8 |
| SC03 | Core | `(499.99, 1)`, nonmember, `SAVE10` | `499.99, 0.00, 499.99, none` | R4, R6, R8 |
| SC04 | Core | `(499.99, 1)`, member, `SAVE10` | `499.99, 25.00, 474.99, member` | R4–R8 |
| SC05 | Core | `(500.00, 1)`, nonmember, `SAVE10` | `500.00, 50.00, 450.00, SAVE10` | R4, R6, R8 |
| SC06 | Core | Member with `SAVE10` and lines `(250.00, 2), (0.01, 1)`. Repeat with reversed lines and with the first line split into two `(250.00, 1)` lines. | Each checkout returns `500.01, 50.00, 450.01, SAVE10` | R4–R8 |
| SC07 | API | JSON prices `12.25`, `"0.50"`, and `0` with quantities 2, 3, and 1. Omit both optional fields. | HTTP 200, money strings worth `26.00, 0.00, 26.00` and label `none` | R2, R4–R6, R8–R9 |
| SC08 | Core | Empty list | `CartValidationError` | R1, R9 |
| SC09 | Core | 101 lines of `(1.00, 1)` | `CartValidationError` | R1, R9 |
| SC10 | API | `items` contains the JSON string `"product"` | HTTP 422 | R1, R9 |
| SC11 | Core | `(-0.01, 1)` | `CartValidationError` | R2, R9 |
| SC12 | Core | `("NaN", 1)` | `CartValidationError` | R2, R9 |
| SC13 | API | `("1.001", 1)` | HTTP 422 | R2, R9 |
| SC14 | Core | `(1000000.01, 1)` | `CartValidationError` | R2, R9 |
| SC15 | Core | `(1.00, 0)` | `CartValidationError` | R3, R9 |
| SC16 | API | `("1.00", true)` | HTTP 422 | R3, R9 |
| SC17 | Core | `(1.00, 10001)` | `CartValidationError` | R3, R9 |
| SC18 | API | `("500.00", 1)`, member, `save10` | HTTP 422 | R6, R9 |

```python
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from api import app
from cart import CartValidationError, calculate_checkout


MONEY_FIELDS = ("subtotal", "discount_amount", "total")


def line(price, quantity=1):
    return {"unit_price": price, "quantity": quantity}


@pytest.mark.parametrize(
    "items, options, expected",
    [
        pytest.param(
            [line("1000000.00", 10000) for _ in range(100)],
            {},
            ("1000000000000.00", "0.00", "1000000000000.00", "none"),
            id="SC01",
        ),
        pytest.param(
            [line("0.10")],
            {"is_member": True},
            ("0.10", "0.01", "0.09", "member"),
            id="SC02",
        ),
        pytest.param(
            [line("499.99")],
            {"coupon": "SAVE10"},
            ("499.99", "0.00", "499.99", "none"),
            id="SC03",
        ),
        pytest.param(
            [line("499.99")],
            {"is_member": True, "coupon": "SAVE10"},
            ("499.99", "25.00", "474.99", "member"),
            id="SC04",
        ),
        pytest.param(
            [line("500.00")],
            {"coupon": "SAVE10"},
            ("500.00", "50.00", "450.00", "SAVE10"),
            id="SC05",
        ),
    ],
)
def test_core_discount_rules(items, options, expected):
    result = calculate_checkout(items, **options)
    assert_core_checkout(result, expected)


def assert_core_checkout(result, expected):
    subtotal, discount, total, label = expected
    assert isinstance(result, dict)
    for field, value in zip(MONEY_FIELDS, (subtotal, discount, total)):
        assert isinstance(result[field], Decimal)
        assert result[field] == Decimal(value)
    assert result["applied_discount"] == label


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
        pytest.param([], id="SC08"),
        pytest.param([line("1.00") for _ in range(101)], id="SC09"),
        pytest.param([line("-0.01")], id="SC11"),
        pytest.param([line("NaN")], id="SC12"),
        pytest.param([line("1000000.01")], id="SC14"),
        pytest.param([line("1.00", 0)], id="SC15"),
        pytest.param([line("1.00", 10001)], id="SC17"),
    ],
)
def test_core_rejects_invalid_items(items):
    with pytest.raises(CartValidationError):
        calculate_checkout(items)


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param({"items": ["product"]}, id="SC10"),
        pytest.param({"items": [line("1.001")]}, id="SC13"),
        pytest.param({"items": [line("1.00", True)]}, id="SC16"),
        pytest.param(
            {"items": [line("500.00")], "is_member": True, "coupon": "save10"},
            id="SC18",
        ),
    ],
)
def test_api_rejects_invalid_inputs(client, payload):
    response = client.post("/checkout", json=payload)
    assert response.status_code == 422
```

## Ambiguity notes

The API requires money strings but leaves their exact formatting open. SC07 checks string types and Decimal values, allowing both `"26"` and `"26.00"`. The specification also leaves open whether a quantity represented as `"1"` or `1.0` may be accepted as an integer.
