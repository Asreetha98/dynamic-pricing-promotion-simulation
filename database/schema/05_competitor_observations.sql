CREATE TABLE IF NOT EXISTS competitor_observations (
    observation_id VARCHAR(70) PRIMARY KEY,
    product_id VARCHAR(20) NOT NULL REFERENCES products(product_id),
    competitor_name VARCHAR(100) NOT NULL,
    competitor_price NUMERIC(12,2) NOT NULL CHECK (competitor_price > 0),
    source_url TEXT,
    observed_at TIMESTAMP NOT NULL,
    received_at TIMESTAMP NOT NULL,
    source_status VARCHAR(20) NOT NULL DEFAULT 'VALID' CHECK (source_status IN ('VALID','STALE','UNVERIFIED')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (received_at >= observed_at)
);
CREATE INDEX IF NOT EXISTS idx_competitor_product_time ON competitor_observations(product_id, observed_at);
