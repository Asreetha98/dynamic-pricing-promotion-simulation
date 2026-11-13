from sqlalchemy import String, DateTime, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base

class Promotion(Base):
    __tablename__ = "promotions"
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    discount_type: Mapped[str] = mapped_column(String(20), nullable=False)  # PERCENT or FIXED
    discount_value: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    starts_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
