"""SmartCart: small, deterministic, specification-driven shopping cart engine.

The business rules and explicit input limits live in docs/requirements.md.
"""

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

CENT = Decimal("0.01")
MEMBER_RATE = Decimal("0.05")
COUPON_RATE = Decimal("0.10")
COUPON_MINIMUM = Decimal("500.00")

# Project-defined guardrails (not limits imposed by the course instructor).
# Keeping input sizes bounded also keeps Decimal arithmetic reliable.
MAX_UNIT_PRICE = Decimal("1000000.00")
MAX_QUANTITY = 10_000
MAX_CART_ITEMS = 100


class CartValidationError(ValueError):
    """Invalid cart, product, membership or coupon data."""


def _price(value):
    """Return a finite, nonnegative amount with at most two meaningful decimals."""
    if isinstance(value, bool):
        raise CartValidationError("Price must be a nonnegative finite amount")
    try:
        amount = Decimal(str(value))
        # Reject NaN and +/-Infinity *before* comparisons or quantization.
        if not amount.is_finite() or amount < 0 or amount > MAX_UNIT_PRICE:
            raise CartValidationError(
                f"Price must be finite and between 0 and {MAX_UNIT_PRICE}"
            )
        if amount != amount.quantize(CENT):
            raise CartValidationError("Price must have at most two decimal places")
    except (InvalidOperation, TypeError, ValueError) as exc:
        if isinstance(exc, CartValidationError):
            raise
        raise CartValidationError("Price must be a valid monetary amount") from exc
    return amount


def calculate_checkout(items, is_member=False, coupon=None):
    """Calculate subtotal, one eligible discount and final total.

    Monetary fields are returned as Decimal (the API serializes them to strings).
    This function has no dependency on a web server or external services.
    """
    if type(is_member) is not bool:
        raise CartValidationError("is_member must be a boolean")
    if coupon not in (None, "SAVE10"):
        raise CartValidationError("Unknown coupon")
    if not isinstance(items, list) or not 1 <= len(items) <= MAX_CART_ITEMS:
        raise CartValidationError(
            f"Cart must contain between 1 and {MAX_CART_ITEMS} items"
        )

    subtotal = Decimal("0.00")
    for item in items:
        if not isinstance(item, dict):
            raise CartValidationError("Each item must be an object")
        qty = item.get("quantity")
        if type(qty) is not int or not 1 <= qty <= MAX_QUANTITY:
            raise CartValidationError(
                f"Quantity must be an integer between 1 and {MAX_QUANTITY}"
            )
        unit_price = _price(item.get("unit_price"))
        subtotal += unit_price * qty

    # Both discounts are computed on the ORIGINAL subtotal and never stack.
    if coupon == "SAVE10" and subtotal >= COUPON_MINIMUM:
        rate, applied = COUPON_RATE, "SAVE10"
    elif is_member:
        rate, applied = MEMBER_RATE, "member"
    else:
        rate, applied = Decimal("0.00"), "none"

    discount = (subtotal * rate).quantize(CENT, rounding=ROUND_HALF_UP)
    total = (subtotal - discount).quantize(CENT)
    return {
        "subtotal": subtotal.quantize(CENT),
        "discount_amount": discount,
        "total": total,
        "applied_discount": applied,
    }
