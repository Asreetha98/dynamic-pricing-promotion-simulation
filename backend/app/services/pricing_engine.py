from decimal import Decimal
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.cost import CostRecord
from app.models.price_history import PriceHistory
from app.models.inventory import InventorySnapshot
from app.models.competitor import CompetitorObservation
from app.models.pricing_decision import PriceDecision
from app.services.promotion_engine import evaluate_promotion
from app.utils.calculations import money, margin_percent

def calculate_price(db: Session, product_id: str, demand_index: float = 1.0,
                    competitor_price: Decimal | None = None, competitor_age_hours: float | None = None,
                    apply_promotion_id: str | None = None):
    product = db.get(Product, product_id)
    if not product:
        raise ValueError("Product not found")

    today = datetime.now(timezone.utc).date()
    cost_record = (db.query(CostRecord).filter(CostRecord.product_id == product_id,
                   CostRecord.effective_from <= today)
                   .order_by(CostRecord.effective_from.desc()).first())
    if not cost_record:
        raise ValueError("No effective cost record exists for this product")
    cost = money(cost_record.unit_cost)

    latest_price = db.query(PriceHistory).filter_by(product_id=product_id).order_by(PriceHistory.effective_from.desc()).first()
    if not latest_price:
        raise ValueError("No price history exists for this product")
    current = money(latest_price.selling_price)

    warnings = []
    if competitor_price is None:
        obs = db.query(CompetitorObservation).filter_by(product_id=product_id).order_by(CompetitorObservation.source_timestamp.desc()).first()
        if obs:
            competitor_price = money(obs.observed_price)
            competitor_age_hours = (datetime.now(timezone.utc) - obs.source_timestamp.replace(tzinfo=timezone.utc)).total_seconds()/3600
    if competitor_price is not None and competitor_age_hours is not None:
        if competitor_age_hours > 24:
            warnings.append("Competitor observation is stale (>24 hours); excluded from pricing signal.")
            competitor_price = None

    # Transparent heuristic: demand and competitor signal adjust the current price.
    multiplier = Decimal("1") + Decimal(str(max(-0.05, min(0.05, (demand_index - 1.0) * 0.05))))
    candidate = money(current * multiplier)
    if competitor_price is not None:
        candidate = money(candidate * Decimal("0.7") + competitor_price * Decimal("0.3"))

    # Inventory pressure: low stock suppresses discounts; excess stock allows a small markdown.
    inv = db.query(InventorySnapshot).filter_by(product_id=product_id).order_by(InventorySnapshot.captured_at.desc()).first()
    if inv:
        available = max(0, inv.quantity_on_hand - inv.quantity_reserved)
        if available == 0:
            warnings.append("Stockout: price decrease blocked.")
            candidate = max(candidate, current)
        elif available > 100:
            candidate = money(candidate * Decimal("0.99"))

    floor_by_margin = money(cost / (Decimal("1") - Decimal(product.min_margin_pct)/Decimal("100")))
    floor = max(money(product.min_price), floor_by_margin)
    ceiling = money(product.max_price)
    if floor > ceiling:
        raise ValueError("Configured price floor exceeds product price ceiling")
    candidate = min(ceiling, max(floor, candidate))

    final_price = candidate
    applied_discount = money(0)
    if apply_promotion_id:
        promo_result = evaluate_promotion(db, apply_promotion_id, product, candidate)
        if not promo_result["eligible"]:
            warnings.append(promo_result["reason"])
        else:
            proposed = money(promo_result["price"])
            # Margin guardrail is applied after discount, using the same unit cost.
            if proposed < floor:
                warnings.append("Promotion blocked: discounted price would violate minimum margin/price floor.")
            else:
                final_price = proposed
                applied_discount = money(promo_result["discount"])

    margin = margin_percent(final_price, cost)
    if margin < Decimal(product.min_margin_pct):
        raise ValueError("Guardrail failure: final margin is below configured minimum")

    decision = "HOLD" if final_price == current else ("INCREASE" if final_price > current else "DECREASE")
    reason = "Candidate derived from demand, competitor and inventory signals; floor/ceiling and post-discount margin checks applied."
    decision_id = f"DEC-{datetime.now(timezone.utc):%Y}-{uuid4().hex[:8].upper()}"
    record = PriceDecision(id=decision_id, product_id=product_id, current_price=current,
        candidate_price=candidate, final_price=final_price, unit_cost=cost, margin_pct=margin,
        decision=decision, reason=reason, inputs={"demand_index": demand_index,
        "competitor_price": str(competitor_price) if competitor_price is not None else None,
        "competitor_age_hours": competitor_age_hours, "inventory_snapshot_id": inv.id if inv else None,
        "promotion_id": apply_promotion_id, "warnings": warnings})
    db.add(record)
    db.commit()
    db.refresh(record)
    return {"product_id": product_id, "current_price": current, "candidate_price": candidate,
        "final_price": final_price, "unit_cost": cost, "margin_pct": margin,
        "decision": decision, "reason": reason, "applied_discount": applied_discount,
        "warnings": warnings, "decision_id": decision_id}
