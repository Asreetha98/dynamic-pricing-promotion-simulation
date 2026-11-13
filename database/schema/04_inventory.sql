CREATE TABLE IF NOT EXISTS inventory_snapshots (
    inventory_snapshot_id VARCHAR(70) PRIMARY KEY,
    product_id VARCHAR(20) NOT NULL REFERENCES products(product_id),
    snapshot_date DATE NOT NULL,
    on_hand_qty INTEGER NOT NULL CHECK (on_hand_qty >= 0),
    reserved_qty INTEGER NOT NULL DEFAULT 0 CHECK (reserved_qty >= 0),
    available_qty INTEGER NOT NULL CHECK (available_qty >= 0),
    daily_demand_qty NUMERIC(10,2) NOT NULL DEFAULT 0 CHECK (daily_demand_qty >= 0),
    stock_status VARCHAR(20) NOT NULL CHECK (stock_status IN ('IN_STOCK','LOW_STOCK','OUT_OF_STOCK')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (available_qty = GREATEST(on_hand_qty - reserved_qty, 0)),
    UNIQUE(product_id, snapshot_date)
);
CREATE INDEX IF NOT EXISTS idx_inventory_date ON inventory_snapshots(snapshot_date);
