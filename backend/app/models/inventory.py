from sqlalchemy import String, DateTime, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.database.base import Base

class InventorySnapshot(Base):
    __tablename__ = "inventory_snapshots"
    __table_args__ = (CheckConstraint("quantity_on_hand >= 0", name="ck_inventory_nonnegative"),)
    id: Mapped[str] = mapped_column(String(70), primary_key=True)
    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"), nullable=False, index=True)
    quantity_on_hand: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity_reserved: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    captured_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
    product = relationship("Product", back_populates="inventory")
