import random
from datetime import date, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.cost import CostRecord
from app.models.price_history import PriceHistory
from app.models.inventory import InventorySnapshot
from app.models.competitor import CompetitorObservation

def generate_products(db: Session, count: int = 25, seed: int = 20261022):
    rng = random.Random(seed)
    created = 0
    for i in range(1, count + 1):
        sku = f"SKU-{i:06d}"
        if db.get(Product, sku): continue
        cost = Decimal(str(round(rng.uniform(20, 500), 2)))
        min_margin = Decimal("15")
        price = (cost / Decimal("0.85")).quantize(Decimal("0.01"))
        product = Product(id=sku, name=f"Product {i:04d}", category=rng.choice(["Electronics", "Home", "Fashion", "Grocery"]),
            brand=rng.choice(["Brand A", "Brand B", "Brand C"]), unit="each",
            min_price=Decimal("1"), max_price=price*Decimal("2"), min_margin_pct=min_margin, is_active=True)
        db.add(product)
        db.add(CostRecord(id=f"COST-{sku}-2026-01", product_id=sku, unit_cost=cost,
                          effective_from=date(2026, 1, 1)))
        db.add(PriceHistory(id=f"PRC-{sku}-20260101", product_id=sku, selling_price=price,
                            effective_from=date(2026, 1, 1), reason="Initial generated price"))
        db.add(InventorySnapshot(id=f"INV-{sku}-20260101", product_id=sku,
                                 quantity_on_hand=rng.randint(0, 250), quantity_reserved=0))
        db.add(CompetitorObservation(id=f"COMP-{sku}-20260101", product_id=sku,
            competitor_name="Competitor A", observed_price=(price*Decimal(str(round(rng.uniform(.9,1.1),2)))).quantize(Decimal("0.01")),
            source_timestamp=__import__("datetime").datetime(2026,1,1)))
        created += 1
    db.commit()
    return {"requested": count, "created": created, "seed": seed}
