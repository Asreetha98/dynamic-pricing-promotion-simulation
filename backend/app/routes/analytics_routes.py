from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services.analytics_engine import get_summary
from app.models.pricing_decision import PriceDecision

router = APIRouter(prefix="/analytics", tags=["Analytics and reports"])

@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    return get_summary(db)

@router.get("/decisions")
def list_decisions(product_id: str | None = None, limit: int = 100, db: Session = Depends(get_db)):
    query = db.query(PriceDecision)
    if product_id:
        query = query.filter(PriceDecision.product_id == product_id)
    rows = query.order_by(PriceDecision.created_at.desc()).limit(min(max(limit, 1), 500)).all()
    return [{"id": r.id, "product_id": r.product_id, "current_price": r.current_price,
             "candidate_price": r.candidate_price, "final_price": r.final_price,
             "unit_cost": r.unit_cost, "margin_pct": r.margin_pct, "decision": r.decision,
             "reason": r.reason, "inputs": r.inputs, "created_at": r.created_at} for r in rows]
