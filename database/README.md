# Dynamic Pricing & Promotion Simulation — Database

## Stack
PostgreSQL + FastAPI/SQLAlchemy integration. This folder is independent of frontend and backend.

## Contents
- `schema/`: PostgreSQL DDL, execute files in numerical order.
- `seed/seed_data.sql`: `\copy` commands to load the generated CSV files.
- `sample_data/`: deterministic synthetic CSV datasets and validation summary.
- `sample_data/ground_truth.csv`: evaluation labels only; never use as model/input features.
- `migrations/`: reserved for future incremental schema changes.

## Generated volume
- Products: 200
- Pricing decision scenarios: 2000 (the requested 2,000 major-case records)
- Promotions: 2000
- Inventory snapshots: 36000
- Total rows across operational CSV files: 43700

The total across all CSV files is greater than 2,000 because each decision is supported by related master, history, promotion and inventory records.

## Setup
1. Create a PostgreSQL database, for example `pricing_simulation`.
2. From this directory, execute each SQL file in `schema/` in numerical order:
   `psql -d pricing_simulation -f schema/01_products.sql` and continue through `09_pricing_decisions.sql`.
3. Load the CSVs using `psql -d pricing_simulation -f seed/seed_data.sql` (run from this directory).
4. Keep `ground_truth.csv` separate from operational tables.

## Deterministic data
- Fixed random seed: `20261022`
- Data is synthetic and uses INR.
- IDs follow stable SKU, COST, PRC, PROMO and DEC conventions.
- Inventory spans 180 daily snapshots per product.
- Competitor observations include deliberately stale samples.
- Anomaly categories include below-floor price, promotion stacking violation, stale competitor signal, margin-before-discount calculation, and missing price-change reason.

## Important implementation notes
- `price_history.decision_id` references `pricing_decisions.decision_id`; therefore create the `price_history` table before `pricing_decisions`, then apply the FK in the final schema file.
- `orders` and `order_items` preserve order header/detail separation.
- `decision_promotions` is the many-to-many bridge between decisions and promotions.
- `ground_truth.csv` is an evaluation artifact and must not be joined into model input features.
- For a production dataset, add exclusion constraints or transactional logic to prevent overlapping effective date ranges for a product's costs/prices.
