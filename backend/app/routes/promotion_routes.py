from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from decimal import Decimal
from app.database.connection import get_db
from app.models.promotion import Promotion
from app.models.promotion_rule import PromotionRule
from app.schemas.promotion_schema import PromotionCreate, PromotionOut

router = APIRouter(prefix="/promotions", tags=["Promotions"])
class PromotionUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    discount_type: str | None = Field(default=None, pattern="^(PERCENT|FIXED)$")
    discount_value: Decimal | None = Field(default=None, gt=0)
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    is_active: bool | None = None

class RuleCreate(BaseModel):
    id: str = Field(min_length=1, max_length=50)
    rule_type: str
    rule_value: str
    is_active: bool = True

@router.post("/", response_model=PromotionOut, status_code=status.HTTP_201_CREATED)
def create_promotion(payload: PromotionCreate, db: Session = Depends(get_db)):
    if db.get(Promotion, payload.id):
        raise HTTPException(409, "Promotion ID already exists")
    row = Promotion(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

@router.get("/", response_model=list[PromotionOut])
def list_promotions(active_only: bool = False, db: Session = Depends(get_db)):
    query = db.query(Promotion)
    if active_only:
        query = query.filter(Promotion.is_active.is_(True))
    return query.order_by(Promotion.starts_at.desc()).all()

@router.get("/{promotion_id}", response_model=PromotionOut)
def get_promotion(promotion_id: str, db: Session = Depends(get_db)):
    row = db.get(Promotion, promotion_id)
    if not row:
        raise HTTPException(404, "Promotion not found")
    return row

@router.post("/{promotion_id}/rules", status_code=status.HTTP_201_CREATED)
def add_rule(promotion_id: str, payload: RuleCreate, db: Session = Depends(get_db)):
    if not db.get(Promotion, promotion_id):
        raise HTTPException(404, "Promotion not found")
    if payload.rule_type not in {"STACKABLE", "MIN_ORDER", "CATEGORY", "EXCLUDE_PROMOTION"}:
        raise HTTPException(422, "Unsupported rule_type")
    if db.get(PromotionRule, payload.id):
        raise HTTPException(409, "Rule ID already exists")
    row = PromotionRule(promotion_id=promotion_id, **payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"id": row.id, "promotion_id": row.promotion_id, "rule_type": row.rule_type,
            "rule_value": row.rule_value, "is_active": row.is_active}

@router.get("/{promotion_id}/rules")
def list_rules(promotion_id: str, db: Session = Depends(get_db)):
    if not db.get(Promotion, promotion_id):
        raise HTTPException(404, "Promotion not found")
    rows = db.query(PromotionRule).filter_by(promotion_id=promotion_id).all()
    return [{"id": r.id, "promotion_id": r.promotion_id, "rule_type": r.rule_type,
             "rule_value": r.rule_value, "is_active": r.is_active} for r in rows]

@router.patch("/{promotion_id}", response_model=PromotionOut)
def update_promotion(promotion_id: str, payload: PromotionUpdate, db: Session = Depends(get_db)):
    row = db.get(Promotion, promotion_id)
    if not row:
        raise HTTPException(404, "Promotion not found")
    updates = payload.model_dump(exclude_unset=True)
    starts_at = updates.get("starts_at", row.starts_at)
    ends_at = updates.get("ends_at", row.ends_at)
    if ends_at <= starts_at:
        raise HTTPException(422, "ends_at must be later than starts_at")
    discount_type = updates.get("discount_type", row.discount_type)
    discount_value = updates.get("discount_value", row.discount_value)
    if discount_type == "PERCENT" and discount_value > 100:
        raise HTTPException(422, "Percentage discount cannot exceed 100")
    for key, value in updates.items():
        setattr(row, key, value)
    db.commit()
    db.refresh(row)
    return row

@router.delete("/{promotion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_promotion(promotion_id: str, db: Session = Depends(get_db)):
    row = db.get(Promotion, promotion_id)
    if not row:
        raise HTTPException(404, "Promotion not found")
    db.query(PromotionRule).filter_by(promotion_id=promotion_id).delete()
    db.delete(row)
    db.commit()
