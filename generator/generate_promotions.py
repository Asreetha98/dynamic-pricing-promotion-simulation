import random
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from sqlalchemy.orm import Session
from app.models.promotion import Promotion

def generate_promotions(db: Session, count: int = 20, seed: int = 20261022):
    rng = random.Random(seed)
    created = 0
    now = datetime.now(timezone.utc)
    for i in range(1, count + 1):
        pid = f"PROMO-{now.year}-{i:06d}"
        if db.get(Promotion, pid): continue
        row = Promotion(id=pid, name=f"Simulation Promotion {i}",
            discount_type="PERCENT", discount_value=Decimal(str(rng.choice([5, 10, 15, 20]))),
            starts_at=now-timedelta(days=1), ends_at=now+timedelta(days=30), is_active=True)
        db.add(row); created += 1
    db.commit()
    return {"requested": count, "created": created, "seed": seed}
