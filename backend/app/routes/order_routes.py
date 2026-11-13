from datetime import datetime, timezone
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.order import Order
from app.models.product import Product
from app.schemas.order_schema import OrderCreate, OrderResponse

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    gross = round(payload.quantity * payload.unit_price, 2)
    if payload.discount_amount > gross:
        raise HTTPException(status_code=422, detail="Discount cannot exceed the order gross amount")
    order = Order(
        id=f"ORD-{datetime.now(timezone.utc):%Y%m%d%H%M%S}-{uuid4().hex[:6].upper()}",
        product_id=payload.product_id, quantity=payload.quantity,
        unit_price=payload.unit_price, discount_amount=payload.discount_amount,
        total_amount=round(gross - payload.discount_amount, 2),
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

@router.get("/", response_model=list[OrderResponse])
def list_orders(product_id: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Order)
    if product_id:
        query = query.filter(Order.product_id == product_id)
    return query.order_by(Order.ordered_at.desc()).all()

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: str, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
