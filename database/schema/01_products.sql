CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(20) PRIMARY KEY,
    sku VARCHAR(20) NOT NULL UNIQUE,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(80) NOT NULL,
    brand VARCHAR(80),
    base_price NUMERIC(12,2) NOT NULL CHECK (base_price > 0),
    price_floor NUMERIC(12,2) NOT NULL CHECK (price_floor > 0),
    price_ceiling NUMERIC(12,2) NOT NULL,
    min_margin_pct NUMERIC(5,2) NOT NULL DEFAULT 10 CHECK (min_margin_pct BETWEEN 0 AND 95),
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE','INACTIVE','DISCONTINUED')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (price_floor <= base_price AND base_price <= price_ceiling)
);
