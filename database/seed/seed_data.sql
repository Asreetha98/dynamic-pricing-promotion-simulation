-- Run schema files in numerical order before loading data.
-- PostgreSQL psql example (run from datadbroot/):
\copy products FROM 'sample_data/products.csv' CSV HEADER;
\copy cost_records FROM 'sample_data/cost_records.csv' CSV HEADER;
\copy price_history FROM 'sample_data/price_history.csv' CSV HEADER;
\copy inventory_snapshots FROM 'sample_data/inventory_snapshots.csv' CSV HEADER;
\copy competitor_observations FROM 'sample_data/competitor_observations.csv' CSV HEADER;
\copy promotions FROM 'sample_data/promotions.csv' CSV HEADER;
\copy promotion_rules FROM 'sample_data/promotion_rules.csv' CSV HEADER;
\copy orders FROM 'sample_data/orders.csv' CSV HEADER;
\copy order_items FROM 'sample_data/order_items.csv' CSV HEADER;
\copy pricing_decisions FROM 'sample_data/pricing_decisions.csv' CSV HEADER;
\copy decision_promotions FROM 'sample_data/decision_promotions.csv' CSV HEADER;

-- ground_truth.csv is evaluation-only. Do NOT load it into operational feature tables.
