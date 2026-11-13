CREATE TABLE IF NOT EXISTS pricing_decisions (
    decision_id VARCHAR(30) PRIMARY KEY,
    product_id VARCHAR(20) NOT NULL REFERENCES products(product_id),
    decision_timestamp TIMESTAMP NOT NULL,
    current_price NUMERIC(12,2) NOT NULL CHECK (current_price > 0),
    candidate_price NUMERIC(12,2) NOT NULL CHECK (candidate_price > 0),
    recommended_price NUMERIC(12,2) NOT NULL CHECK (recommended_price > 0),
    unit_cost NUMERIC(12,2) NOT NULL CHECK (unit_cost > 0),
    expected_demand_qty NUMERIC(10,2) NOT NULL CHECK (expected_demand_qty >= 0),
    available_stock INTEGER NOT NULL CHECK (available_stock >= 0),
    competitor_price NUMERIC(12,2),
    competitor_observation_id VARCHAR(70) REFERENCES competitor_observations(observation_id),
    applied_discount NUMERIC(12,2) NOT NULL DEFAULT 0 CHECK (applied_discount >= 0),
    realized_margin_pct NUMERIC(7,2) NOT NULL,
    decision_status VARCHAR(20) NOT NULL CHECK (decision_status IN ('APPROVED','BLOCKED','REVIEW','APPLIED')),
    decision_reason TEXT NOT NULL,
    issue_type VARCHAR(60) NOT NULL DEFAULT 'NONE',
    ground_truth_label VARCHAR(40) NOT NULL DEFAULT 'VALID',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_decision_product_time ON pricing_decisions(product_id, decision_timestamp);
CREATE INDEX IF NOT EXISTS idx_decision_issue ON pricing_decisions(issue_type);
ALTER TABLE price_history
    ADD CONSTRAINT fk_price_history_decision
    FOREIGN KEY (decision_id) REFERENCES pricing_decisions(decision_id);
CREATE TABLE IF NOT EXISTS decision_promotions (
    decision_id VARCHAR(30) NOT NULL REFERENCES pricing_decisions(decision_id),
    promotion_id VARCHAR(30) NOT NULL REFERENCES promotions(promotion_id),
    applied_discount NUMERIC(12,2) NOT NULL DEFAULT 0 CHECK (applied_discount >= 0),
    application_status VARCHAR(20) NOT NULL CHECK (application_status IN ('APPLIED','REJECTED','EVALUATED')),
    PRIMARY KEY(decision_id, promotion_id)
);
