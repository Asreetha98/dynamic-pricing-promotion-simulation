from decimal import Decimal
from app.utils.calculations import discount_price

def test_fixed_discount_never_negative():
    assert discount_price(Decimal("10"), "FIXED", Decimal("20")) == Decimal("0.00")
