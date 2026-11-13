CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(30) PRIMARY KEY,
    order_date TIMESTAMP NOT NULL,
    customer_ref VARCHAR(40) NOT NULL,
    order_status VARCHAR(20) NOT NULL CHECK (order_status IN ('PLACED','PAID','SHIPPED','CANCELLED','RETURNED')),
    subtotal NUMERIC(12,2) NOT NULL CHECK (subtotal >= 0),
    discount_total NUMERIC(12,2) NOT NULL DEFAULT 0 CHECK (discount_total >= 0),
    grand_total NUMERIC(12,2) NOT NULL CHECK (grand_total >= 0),
    currency CHAR(3) NOT NULL DEFAULT 'INR',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (grand_total = GREATEST(subtotal - discount_total, 0))
);
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id VARCHAR(40) PRIMARY KEY,
    order_id VARCHAR(30) NOT NULL REFERENCES orders(order_id),
    product_id VARCHAR(20) NOT NULL REFERENCES products(product_id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(12,2) NOT NULL CHECK (unit_price > 0),
    line_discount NUMERIC(12,2) NOT NULL DEFAULT 0 CHECK (line_discount >= 0),
    line_total NUMERIC(12,2) NOT NULL CHECK (line_total >= 0),
    CHECK (line_total = GREATEST(quantity * unit_price - line_discount, 0))
);
