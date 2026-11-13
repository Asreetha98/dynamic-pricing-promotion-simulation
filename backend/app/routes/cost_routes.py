from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.cost import CostRecord
from app.models.product import Product
from app.schemas.cost_schema import CostCreate, CostResponse

router = APIRouter(prefix="/costs", tags=["Cost Records"])

@router.post("/", response_model=CostResponse, status_code=status.HTTP_201_CREATED)
def create_cost(payload: CostCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    cost_id = f"COST-{payload.product_id}-{payload.effective_from:%Y%m%d}"
    if db.query(CostRecord).filter(CostRecord.id == cost_id).first():
        raise HTTPException(status_code=409, detail="A cost record already exists for this product and effective date")
    record = CostRecord(id=cost_id, product_id=payload.product_id,
                        unit_cost=payload.unit_cost, effective_from=payload.effective_from,
                        effective_to=payload.effective_to)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/", response_model=list[CostResponse])
def list_costs(product_id: str | None = None, db: Session = Depends(get_db)):
    query = db.query(CostRecord)
    if product_id:
        query = query.filter(CostRecord.product_id == product_id)
    return query.order_by(CostRecord.effective_from.desc()).all()

@router.get("/{cost_id}", response_model=CostResponse)
def get_cost(cost_id: str, db: Session = Depends(get_db)):
    record = db.get(CostRecord, cost_id)
    if not record:
        raise HTTPException(status_code=404, detail="Cost record not found")
    return record
