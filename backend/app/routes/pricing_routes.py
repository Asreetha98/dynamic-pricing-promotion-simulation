from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.pricing_schema import PricingRequest
from app.services.pricing_engine import calculate_price

router = APIRouter(prefix="/pricing", tags=["Pricing simulation"])

@router.post("/simulate")
def simulate_price(payload: PricingRequest, db: Session = Depends(get_db)):
    try:
        return calculate_price(db, **payload.model_dump())
    except ValueError as exc:
        raise HTTPException(400, str(exc))
