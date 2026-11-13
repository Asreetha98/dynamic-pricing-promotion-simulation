CREATE TABLE IF NOT EXISTS promotions (
    promotion_id VARCHAR(30) PRIMARY KEY,
    promotion_name VARCHAR(150) NOT NULL,
    promotion_type VARCHAR(20) NOT NULL CHECK (promotion_type IN ('PERCENT','FIXED','COUPON')),
    discount_value NUMERIC(10,2) NOT NULL CHECK (discount_value > 0),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('DRAFT','SCHEDULED','ACTIVE','EXPIRED','CANCELLED')),
    stackable BOOLEAN NOT NULL DEFAULT FALSE,
    max_discount_amount NUMERIC(12,2),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (end_date >= start_date),
    CHECK (promotion_type <> 'PERCENT' OR discount_value <= 100)
);
