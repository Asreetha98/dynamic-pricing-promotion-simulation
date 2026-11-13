from datetime import date
from pydantic import BaseModel, ConfigDict, Field, model_validator

class CostCreate(BaseModel):
    product_id: str = Field(min_length=1, max_length=30)
    unit_cost: float = Field(gt=0)
    effective_from: date
    effective_to: date | None = None

    @model_validator(mode="after")
    def validate_dates(self):
        if self.effective_to and self.effective_to < self.effective_from:
            raise ValueError("effective_to cannot be earlier than effective_from")
        return self

class CostResponse(BaseModel):
    id: str
    product_id: str
    unit_cost: float
    effective_from: date
    effective_to: date | None
    model_config = ConfigDict(from_attributes=True)
