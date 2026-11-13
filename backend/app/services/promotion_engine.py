from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy.orm import Session
from app.models.promotion import Promotion
from app.models.promotion_rule import PromotionRule
from app.utils.calculations import discount_price, money

def evaluate_promotion(db: Session, promotion_id: str, product, base_price: Decimal,
                       order_value: Decimal | None = None, now: datetime | None = None):
    now = now or datetime.now(timezone.utc)
    promo = db.get(Promotion, promotion_id)
    if not promo:
        return {"eligible": False, "reason": "Promotion not found", "discount": money(0), "price": base_price}
    if not promo.is_active or not (promo.starts_at <= now <= promo.ends_at):
        return {"eligible": False, "reason": "Promotion is inactive or outside its validity period", "discount": money(0), "price": base_price}

    rules = db.query(PromotionRule).filter_by(promotion_id=promotion_id, is_active=True).all()
    for rule in rules:
        if rule.rule_type == "MIN_ORDER":
            if order_value is None or order_value < Decimal(rule.rule_value):
                return {"eligible": False, "reason": f"Minimum order value {rule.rule_value} not met", "discount": money(0), "price": base_price}
        elif rule.rule_type == "CATEGORY" and product.category != rule.rule_value:
            return {"eligible": False, "reason": "Product category is not eligible", "discount": money(0), "price": base_price}

    discounted = discount_price(base_price, promo.discount_type, Decimal(promo.discount_value))
    return {"eligible": True, "reason": "Promotion eligible", "discount": money(base_price-discounted), "price": discounted, "promotion_id": promo.id}
