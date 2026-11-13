from datetime import datetime, timezone
from uuid import uuid4
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.product import Product
from app.models.competitor import CompetitorObservation

router = APIRouter(prefix="/competitors", tags=["Competitor observations"])
class ObservationCreate(BaseModel):
    product_id: str
    competitor_name: str = Field(min_length=1, max_length=100)
    observed_price: Decimal = Field(gt=0)
    source_url: str | None = None
    source_timestamp: datetime

@router.post("/", status_code=201)
def add_observation(payload: ObservationCreate, db: Session = Depends(get_db)):
    if not db.get(Product, payload.product_id):
        raise HTTPException(404, "Product not found")
    row = CompetitorObservation(id=f"COMP-{datetime.now(timezone.utc):%Y%m%d%H%M%S}-{uuid4().hex[:6].upper()}", **payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return observation_out(row)

def observation_out(row):
    return {"id": row.id, "product_id": row.product_id, "competitor_name": row.competitor_name,
            "observed_price": row.observed_price, "source_url": row.source_url,
            "source_timestamp": row.source_timestamp, "recorded_at": row.recorded_at}

@router.get("/")
def list_observations(product_id: str | None = None, limit: int = 100, db: Session = Depends(get_db)):
    query = db.query(CompetitorObservation)
    if product_id:
        query = query.filter(CompetitorObservation.product_id == product_id)
    return [observation_out(x) for x in query.order_by(CompetitorObservation.source_timestamp.desc()).limit(min(max(limit, 1), 500)).all()]
