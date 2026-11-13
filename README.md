<<<<<<< HEAD
# Dynamic Pricing and Promotion Simulation

This combines the supplied database, FastAPI backend, and React frontend into one runnable project. The `database/` directory preserves the full PostgreSQL analytical schema and synthetic CSV dataset. The backend runs locally on SQLite by default and uses its own SQLAlchemy prototype schema; these schemas are not interchangeable. Use the CSV loader below for a local demo, or load the original database independently into PostgreSQL using `database/README.md`.

## Requirements

- Python 3.10+
- Node.js 18+ and npm

## Run locally

In Terminal 1:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env            # Windows: copy .env.example .env
python seed_sample_data.py      # Optional; imports sample CSV data into SQLite
uvicorn app.main:app --reload
```

In Terminal 2:

```bash
cd frontend
npm install
cp .env.example .env            # Windows: copy .env.example .env
npm run dev
```

Open http://localhost:5173. Backend docs are at http://127.0.0.1:8000/docs and health check at http://127.0.0.1:8000/health. Frontend `.env` uses `VITE_API_BASE_URL=http://127.0.0.1:8000/api` and `VITE_USE_MOCK_DATA=false`; switch mock data on explicitly with `true` if desired.

The loader imports products, costs, latest prices, the latest inventory snapshot for each product, competitor observations and promotions. It intentionally leaves evaluation-only `ground_truth.csv` out of the operational database. It will not overwrite an existing populated SQLite database; remove `backend/pricing_simulation.db` if you want to reload from scratch.

## Database archive

The provided SQL schema and its CSVs are a separate, richer PostgreSQL analysis dataset with its own column names and entities. Follow `database/README.md` to initialize it. `database/seed/seed_data.sql` uses `psql`'s `\\copy` and must be run from the combined project root so its `sample_data/...` paths resolve. Do not run those DDL files against the backend SQLite database.

## Main backend paths

- `backend/app/`: API, database models, pricing and promotion logic
- `frontend/src/`: React interface and API adapter
- `database/schema/`, `database/sample_data/`: original SQL schema and generated dataset

The demo backend exposes product, inventory, competitor, promotion, pricing, and analytics endpoints. Its pricing engine persists simulation decisions. The independent CSV analysis dataset includes order-level and decision ground truth not yet represented in the backend ORM.
=======
# dynamic-pricing-promotion-simulation
>>>>>>> origin/master
