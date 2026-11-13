from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, model_validator
from decimal import Decimal
from app.database.connection import get_db
from app.models.product import Product
from app.schemas.product_schema import ProductCreate, ProductOut

router = APIRouter(prefix="/products", tags=["Products"])

class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    category: str | None = None
    brand: str | None = None
    unit: str | None = None
    min_price: Decimal | None = Field(default=None, ge=0)
    max_price: Decimal | None = Field(default=None, gt=0)
    min_margin_pct: Decimal | None = Field(default=None, ge=0, le=99)
    is_active: bool | None = None

@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    if payload.max_price < payload.min_price:
        raise HTTPException(422, "max_price must be greater than or equal to min_price")
    if db.get(Product, payload.id):
        raise HTTPException(409, "Product ID already exists")
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.get("/", response_model=list[ProductOut])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if skip < 0 or limit < 1:
        raise HTTPException(422, "skip must be >= 0 and limit must be >= 1")
    return db.query(Product).order_by(Product.id).offset(skip).limit(min(limit, 500)).all()

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: str, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    return product

@router.patch("/{product_id}", response_model=ProductOut)
def update_product(product_id: str, payload: ProductUpdate, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    updates = payload.model_dump(exclude_unset=True)
    min_price = updates.get("min_price", product.min_price)
    max_price = updates.get("max_price", product.max_price)
    if max_price < min_price:
        raise HTTPException(422, "max_price must be greater than or equal to min_price")
    for key, value in updates.items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: str, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    try:
        db.delete(product)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(409, "Product cannot be deleted because related records exist")
