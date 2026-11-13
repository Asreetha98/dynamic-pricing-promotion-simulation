from pydantic import BaseModel, Field
from decimal import Decimal

class PricingRequest(BaseModel):
    product_id: str
    demand_index: float = Field(default=1.0, ge=0, le=3)
    competitor_price: Decimal | None = Field(default=None, gt=0)
    competitor_age_hours: float | None = Field(default=None, ge=0)
    apply_promotion_id: str | None = None

class PricingResult(BaseModel):
    product_id: str
    current_price: Decimal
    candidate_price: Decimal
    final_price: Decimal
    unit_cost: Decimal
    margin_pct: Decimal
    decision: str
    reason: str
    applied_discount: Decimal
    warnings: list[str]
