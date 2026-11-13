from sqlalchemy import String, Boolean, DateTime, Numeric, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.database.base import Base

class Product(Base):
    __tablename__ = "products"
    id: Mapped[str] = mapped_column(String(30), primary_key=True)  # SKU-000001
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    category: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    brand: Mapped[str | None] = mapped_column(String(80))
    unit: Mapped[str] = mapped_column(String(20), default="each")
    min_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    max_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    min_margin_pct: Mapped[float] = mapped_column(Numeric(6, 2), nullable=False, default=10)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    costs = relationship("CostRecord", back_populates="product", cascade="all, delete-orphan")
    prices = relationship("PriceHistory", back_populates="product", cascade="all, delete-orphan")
    inventory = relationship("InventorySnapshot", back_populates="product", cascade="all, delete-orphan")
