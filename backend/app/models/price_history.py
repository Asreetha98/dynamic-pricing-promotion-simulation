from sqlalchemy import String, Date, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.database.base import Base

class PriceHistory(Base):
    __tablename__ = "price_history"
    id: Mapped[str] = mapped_column(String(70), primary_key=True)
    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"), nullable=False, index=True)
    selling_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    effective_from: Mapped[Date] = mapped_column(Date, nullable=False)
    reason: Mapped[str] = mapped_column(String(250), nullable=False)
    product = relationship("Product", back_populates="prices")
