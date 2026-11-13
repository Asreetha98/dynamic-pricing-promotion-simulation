from decimal import Decimal, ROUND_HALF_UP

CENT = Decimal("0.01")

def money(value) -> Decimal:
    return Decimal(str(value)).quantize(CENT, rounding=ROUND_HALF_UP)

def margin_percent(price: Decimal, cost: Decimal) -> Decimal:
    if price <= 0:
        return Decimal("0")
    return ((price - cost) / price * Decimal("100")).quantize(CENT, rounding=ROUND_HALF_UP)

def discount_price(price: Decimal, discount_type: str, discount_value: Decimal) -> Decimal:
    if discount_type == "PERCENT":
        return money(price * (Decimal("1") - discount_value / Decimal("100")))
    if discount_type == "FIXED":
        return max(Decimal("0"), money(price - discount_value))
    raise ValueError("Unsupported discount type")
