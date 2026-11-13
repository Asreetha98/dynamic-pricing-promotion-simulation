CREATE TABLE IF NOT EXISTS promotion_rules (
    rule_id VARCHAR(40) PRIMARY KEY,
    promotion_id VARCHAR(30) NOT NULL REFERENCES promotions(promotion_id),
    rule_type VARCHAR(30) NOT NULL CHECK (rule_type IN ('MIN_CART_VALUE','CATEGORY_IN','CATEGORY_EXCLUDE','STACK_EXCLUDE','MIN_MARGIN','MAX_DISCOUNT')),
    rule_value TEXT NOT NULL,
    is_hard_block BOOLEAN NOT NULL DEFAULT TRUE,
    priority INTEGER NOT NULL DEFAULT 100,
    effective_from DATE NOT NULL,
    effective_to DATE,
    CHECK (effective_to IS NULL OR effective_to >= effective_from)
);
