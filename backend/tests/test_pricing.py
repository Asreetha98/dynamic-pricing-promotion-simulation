from decimal import Decimal
from app.utils.calculations import margin_percent, discount_price

def test_margin_uses_discounted_selling_price():
    assert margin_percent(Decimal("90"), Decimal("60")) == Decimal("33.33")

def test_percentage_discount():
    assert discount_price(Decimal("100"), "PERCENT", Decimal("10")) == Decimal("90.00")
