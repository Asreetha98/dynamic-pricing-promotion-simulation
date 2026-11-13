from sqlalchemy import func
from app.models.pricing_decision import PriceDecision
from app.models.product import Product

def get_summary(db):
    total_products = db.query(func.count(Product.id)).scalar() or 0
    total_decisions = db.query(func.count(PriceDecision.id)).scalar() or 0
    avg_margin = db.query(func.avg(PriceDecision.margin_pct)).scalar()
    blocked = db.query(func.count(PriceDecision.id)).filter(PriceDecision.decision == "BLOCKED").scalar() or 0
    return {"total_products": total_products, "total_decisions": total_decisions,
            "average_margin_pct": round(float(avg_margin or 0), 2), "blocked_decisions": blocked}
