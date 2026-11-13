from sqlalchemy import String, Date, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.database.base import Base

class CostRecord(Base):
    __tablename__ = "cost_records"
    id: Mapped[str] = mapped_column(String(60), primary_key=True)
    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"), nullable=False, index=True)
    unit_cost: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    effective_from: Mapped[Date] = mapped_column(Date, nullable=False)
    effective_to: Mapped[Date | None] = mapped_column(Date)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    product = relationship("Product", back_populates="costs")
