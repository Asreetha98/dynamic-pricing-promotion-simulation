from sqlalchemy import String, DateTime, Numeric, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.database.base import Base

class PriceDecision(Base):
    __tablename__ = "price_decisions"
    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"), nullable=False, index=True)
    current_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    candidate_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    final_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    unit_cost: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    margin_pct: Mapped[float] = mapped_column(Numeric(7, 2), nullable=False)
    decision: Mapped[str] = mapped_column(String(30), nullable=False)  # INCREASE, DECREASE, HOLD, BLOCKED
    reason: Mapped[str] = mapped_column(String(500), nullable=False)
    inputs: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
