from datetime import datetime, timezone
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.product import Product
from app.models.inventory import InventorySnapshot

router = APIRouter(prefix="/inventory", tags=["Inventory"])
class InventoryCreate(BaseModel):
    product_id: str
    quantity_on_hand: int = Field(ge=0)
    quantity_reserved: int = Field(default=0, ge=0)

@router.post("/", status_code=201)
def create_snapshot(payload: InventoryCreate, db: Session = Depends(get_db)):
    if not db.get(Product, payload.product_id):
        raise HTTPException(404, "Product not found")
    if payload.quantity_reserved > payload.quantity_on_hand:
        raise HTTPException(422, "Reserved quantity cannot exceed on-hand quantity")
    row = InventorySnapshot(id=f"INV-{datetime.now(timezone.utc):%Y%m%d%H%M%S}-{uuid4().hex[:6].upper()}",
        **payload.model_dump(), captured_at=datetime.now(timezone.utc))
    db.add(row)
    db.commit()
    db.refresh(row)
    return inventory_out(row)

def inventory_out(row):
    return {"id": row.id, "product_id": row.product_id, "quantity_on_hand": row.quantity_on_hand,
            "quantity_reserved": row.quantity_reserved, "available": row.quantity_on_hand-row.quantity_reserved,
            "captured_at": row.captured_at}

@router.get("/")
def list_inventory(product_id: str | None = None, limit: int = 100, db: Session = Depends(get_db)):
    query = db.query(InventorySnapshot)
    if product_id:
        query = query.filter(InventorySnapshot.product_id == product_id)
    return [inventory_out(x) for x in query.order_by(InventorySnapshot.captured_at.desc()).limit(min(max(limit, 1), 500)).all()]

@router.get("/{product_id}/latest")
def latest_inventory(product_id: str, db: Session = Depends(get_db)):
    row = db.query(InventorySnapshot).filter_by(product_id=product_id).order_by(InventorySnapshot.captured_at.desc()).first()
    if not row:
        raise HTTPException(404, "Inventory snapshot not found")
    return inventory_out(row)
