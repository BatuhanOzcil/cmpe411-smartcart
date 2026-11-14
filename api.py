"""FastAPI checkout endpoint: the API/integration level of SmartCart tests."""

from decimal import Decimal
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from cart import (
    CartValidationError,
    MAX_CART_ITEMS,
    MAX_QUANTITY,
    MAX_UNIT_PRICE,
    calculate_checkout,
)

app = FastAPI(title="SmartCart CMPE 411")


class LineItem(BaseModel):
    unit_price: Decimal = Field(ge=0, le=MAX_UNIT_PRICE, decimal_places=2)
    quantity: int = Field(gt=0, le=MAX_QUANTITY, strict=True)


class CheckoutRequest(BaseModel):
    items: list[LineItem] = Field(min_length=1, max_length=MAX_CART_ITEMS)
    is_member: bool = Field(default=False, strict=True)
    coupon: Literal["SAVE10"] | None = None


class CheckoutResponse(BaseModel):
    subtotal: Decimal
    discount_amount: Decimal
    total: Decimal
    applied_discount: str


@app.post("/checkout", response_model=CheckoutResponse)
def checkout_endpoint(request: CheckoutRequest):
    try:
        return calculate_checkout(
            [item.model_dump() for item in request.items],
            is_member=request.is_member,
            coupon=request.coupon,
        )
    except CartValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
