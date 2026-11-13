from sqlalchemy import String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.database.base import Base

class CompetitorObservation(Base):
    __tablename__ = "competitor_observations"
    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"), nullable=False, index=True)
    competitor_name: Mapped[str] = mapped_column(String(100), nullable=False)
    observed_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    source_url: Mapped[str | None] = mapped_column(String(500))
    source_timestamp: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    recorded_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
