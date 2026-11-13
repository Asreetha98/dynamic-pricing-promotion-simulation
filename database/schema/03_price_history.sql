CREATE TABLE IF NOT EXISTS price_history (
    price_history_id VARCHAR(70) PRIMARY KEY,
    product_id VARCHAR(20) NOT NULL REFERENCES products(product_id),
    selling_price NUMERIC(12,2) NOT NULL CHECK (selling_price > 0),
    valid_from TIMESTAMP NOT NULL,
    valid_to TIMESTAMP,
    change_reason VARCHAR(120),
    changed_by VARCHAR(80) NOT NULL DEFAULT 'SYSTEM',
    decision_id VARCHAR(30),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (valid_to IS NULL OR valid_to >= valid_from)
);
CREATE INDEX IF NOT EXISTS idx_price_product_valid ON price_history(product_id, valid_from);
