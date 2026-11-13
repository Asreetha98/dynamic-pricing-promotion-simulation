from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class OrderCreate(BaseModel):
    product_id: str = Field(min_length=1, max_length=30)
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)
    discount_amount: float = Field(default=0, ge=0)

class OrderResponse(BaseModel):
    id: str
    product_id: str
    quantity: int
    unit_price: float
    discount_amount: float
    total_amount: float
    ordered_at: datetime | None = None
    model_config = ConfigDict(from_attributes=True)
