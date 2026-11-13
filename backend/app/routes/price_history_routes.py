from datetime import date
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.product import Product
from app.models.price_history import PriceHistory

router = APIRouter(prefix="/price-history", tags=["Price history"])

class PriceHistoryCreate(BaseModel):
    product_id: str
    selling_price: float = Field(gt=0)
    effective_from: date
    reason: str = Field(min_length=3, max_length=250)

@router.post("/", status_code=201)
def create_price_history(payload: PriceHistoryCreate, db: Session = Depends(get_db)):
    if not db.get(Product, payload.product_id):
        raise HTTPException(404, "Product not found")
    row = PriceHistory(id=f"PRC-{payload.product_id}-{payload.effective_from:%Y%m%d}-{uuid4().hex[:4].upper()}",
                       **payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return price_out(row)

def price_out(row):
    return {"id": row.id, "product_id": row.product_id, "selling_price": row.selling_price,
            "effective_from": row.effective_from, "reason": row.reason}

@router.get("/")
def list_price_history(product_id: str | None = None, limit: int = 100, db: Session = Depends(get_db)):
    query = db.query(PriceHistory)
    if product_id:
        query = query.filter(PriceHistory.product_id == product_id)
    rows = query.order_by(PriceHistory.effective_from.desc()).limit(min(max(limit, 1), 500)).all()
    return [price_out(row) for row in rows]
