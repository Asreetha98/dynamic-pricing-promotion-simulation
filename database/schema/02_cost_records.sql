CREATE TABLE IF NOT EXISTS cost_records (
    cost_id VARCHAR(60) PRIMARY KEY,
    product_id VARCHAR(20) NOT NULL REFERENCES products(product_id),
    unit_cost NUMERIC(12,2) NOT NULL CHECK (unit_cost > 0),
    currency CHAR(3) NOT NULL DEFAULT 'INR',
    effective_from DATE NOT NULL,
    effective_to DATE,
    source VARCHAR(80) NOT NULL DEFAULT 'SYNTHETIC',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (effective_to IS NULL OR effective_to >= effective_from),
    UNIQUE(product_id, effective_from)
);
CREATE INDEX IF NOT EXISTS idx_cost_product_dates ON cost_records(product_id, effective_from, effective_to);
