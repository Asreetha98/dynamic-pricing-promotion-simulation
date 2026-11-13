from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database.base import Base
from app.database.connection import get_db

@pytest.fixture()
def client():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)
    def override_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()

def create_product(client):
    response = client.post("/api/products/", json={
        "id": "SKU-000001", "name": "Test Laptop", "category": "Electronics",
        "brand": "Demo", "unit": "each", "min_price": "100.00",
        "max_price": "2000.00", "min_margin_pct": "10.00", "is_active": True
    })
    assert response.status_code == 201, response.text

def test_post_and_get_product(client):
    create_product(client)
    assert client.get("/api/products/SKU-000001").status_code == 200
    assert client.get("/api/products/").json()[0]["id"] == "SKU-000001"

def test_post_cost_inventory_competitor_and_order(client):
    create_product(client)
    cost = client.post("/api/costs/", json={"product_id":"SKU-000001", "unit_cost":500,
        "effective_from":date.today().isoformat()})
    assert cost.status_code == 201, cost.text
    inventory = client.post("/api/inventory/", json={"product_id":"SKU-000001", "quantity_on_hand":50, "quantity_reserved":5})
    assert inventory.status_code == 201, inventory.text
    assert inventory.json()["available"] == 45
    competitor = client.post("/api/competitors/", json={"product_id":"SKU-000001", "competitor_name":"Rival",
        "observed_price":"850.00", "source_timestamp":datetime.now(timezone.utc).isoformat()})
    assert competitor.status_code == 201, competitor.text
    order = client.post("/api/orders/", json={"product_id":"SKU-000001", "quantity":2, "unit_price":900, "discount_amount":50})
    assert order.status_code == 201, order.text
    assert float(order.json()["total_amount"]) == 1750.0

def test_post_promotion_and_rule(client):
    start = datetime.now(timezone.utc)
    promo = client.post("/api/promotions/", json={"id":"PROMO-TEST-001", "name":"Test sale",
        "discount_type":"PERCENT", "discount_value":"5", "starts_at":start.isoformat(),
        "ends_at":(start+timedelta(days=3)).isoformat(), "is_active":True})
    assert promo.status_code == 201, promo.text
    rule = client.post("/api/promotions/PROMO-TEST-001/rules", json={"id":"RULE-TEST-001",
        "rule_type":"MIN_ORDER", "rule_value":"500", "is_active":True})
    assert rule.status_code == 201, rule.text
    assert len(client.get("/api/promotions/PROMO-TEST-001/rules").json()) == 1

def test_product_patch_and_delete(client):
    create_product(client)
    changed = client.patch("/api/products/SKU-000001", json={"id":"SKU-000001", "name":"Updated Laptop",
        "category":"Electronics", "brand":"Demo", "unit":"each", "min_price":"100",
        "max_price":"2100", "min_margin_pct":"10", "is_active":True})
    assert changed.status_code == 200, changed.text
    assert changed.json()["name"] == "Updated Laptop"
    deleted = client.delete("/api/products/SKU-000001")
    assert deleted.status_code == 204

def test_post_price_history_and_pricing_simulation(client):
    create_product(client)
    cost = client.post("/api/costs/", json={"product_id":"SKU-000001", "unit_cost":500,
        "effective_from":date.today().isoformat()})
    assert cost.status_code == 201, cost.text
    price = client.post("/api/price-history/", json={"product_id":"SKU-000001", "selling_price":900,
        "effective_from":date.today().isoformat(), "reason":"Initial selling price"})
    assert price.status_code == 201, price.text
    result = client.post("/api/pricing/simulate", json={"product_id":"SKU-000001", "demand_index":1.1})
    assert result.status_code == 200, result.text
    assert result.json()["decision_id"].startswith("DEC-")
    decisions = client.get("/api/analytics/decisions").json()
    assert len(decisions) == 1
