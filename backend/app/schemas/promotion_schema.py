from pydantic import BaseModel, Field, ConfigDict, model_validator
from datetime import datetime
from decimal import Decimal

class PromotionCreate(BaseModel):
    id: str
    name: str
    discount_type: str = Field(pattern="^(PERCENT|FIXED)$")
    discount_value: Decimal = Field(gt=0)
    starts_at: datetime
    ends_at: datetime
    is_active: bool = True

    @model_validator(mode="after")
    def validate_dates(self):
        if self.ends_at <= self.starts_at:
            raise ValueError("ends_at must be later than starts_at")
        if self.discount_type == "PERCENT" and self.discount_value > 100:
            raise ValueError("Percentage discount cannot exceed 100")
        return self

class PromotionOut(PromotionCreate):
    model_config = ConfigDict(from_attributes=True)
