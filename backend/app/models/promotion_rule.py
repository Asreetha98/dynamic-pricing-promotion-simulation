from sqlalchemy import String, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base

class PromotionRule(Base):
    __tablename__ = "promotion_rules"
    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    promotion_id: Mapped[str] = mapped_column(ForeignKey("promotions.id"), nullable=False, index=True)
    rule_type: Mapped[str] = mapped_column(String(30), nullable=False)  # STACKABLE, MIN_ORDER, CATEGORY, EXCLUDE_PROMOTION
    rule_value: Mapped[str] = mapped_column(String(150), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
