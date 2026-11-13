from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal

class ProductCreate(BaseModel):
    id: str = Field(pattern=r"^SKU-\d{6}$")
    name: str = Field(min_length=2, max_length=150)
    category: str
    brand: str | None = None
    unit: str = "each"
    min_price: Decimal = Field(ge=0)
    max_price: Decimal = Field(gt=0)
    min_margin_pct: Decimal = Field(ge=0, le=99)
    is_active: bool = True

class ProductOut(ProductCreate):
    model_config = ConfigDict(from_attributes=True)
