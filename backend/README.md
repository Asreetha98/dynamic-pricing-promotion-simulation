# Dynamic Pricing and Promotion Simulation System — Backend v3

FastAPI + SQLAlchemy backend with working create/read/update/delete APIs for the core project modules. API routes use the `/api` prefix.

## 1. Setup (macOS)

From the project root (the folder containing `backend/` and `.venv/`):

```bash
source .venv/bin/activate
cd backend
pip install -r requirements.txt
cp .env.example .env   # only if .env does not already exist
python -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` and `http://127.0.0.1:8000/health`.

If you run from the project root instead, use:

```bash
python -m uvicorn app.main:app --reload --app-dir backend
```

## 2. API endpoints

All endpoints below are prefixed with `/api`.

| Module | Method | Endpoint | Purpose |
|---|---|---|---|
| Auth | POST | `/auth/register` | Register analyst account |
| Auth | POST | `/auth/login` | Login and receive JWT |
| Auth | GET | `/auth/me` | Get current logged-in user |
| Products | POST | `/products/` | Create product |
| Products | GET | `/products/` | List products |
| Products | GET | `/products/{product_id}` | Get one product |
| Products | PATCH | `/products/{product_id}` | Update product |
| Products | DELETE | `/products/{product_id}` | Delete product if no dependent records exist |
| Costs | POST | `/costs/` | Add effective-dated cost record |
| Price history | POST | `/price-history/` | Add effective-dated selling price (required before simulation) |
| Price history | GET | `/price-history/` | List price history (optional `product_id`) |
| Costs | GET | `/costs/` | List cost records (optional `product_id`) |
| Costs | GET | `/costs/{cost_id}` | Get cost record |
| Inventory | POST | `/inventory/` | Add inventory snapshot |
| Inventory | GET | `/inventory/` | List snapshots (optional `product_id`) |
| Inventory | GET | `/inventory/{product_id}/latest` | Get latest product stock |
| Competitors | POST | `/competitors/` | Add competitor observation |
| Competitors | GET | `/competitors/` | List observations (optional `product_id`) |
| Promotions | POST | `/promotions/` | Create promotion |
| Promotions | GET | `/promotions/` | List promotions (`active_only=true` optional) |
| Promotions | GET | `/promotions/{promotion_id}` | Get one promotion |
| Promotions | PATCH | `/promotions/{promotion_id}` | Update promotion |
| Promotions | DELETE | `/promotions/{promotion_id}` | Delete promotion and its rules |
| Promotion rules | POST | `/promotions/{promotion_id}/rules` | Add promotion rule |
| Promotion rules | GET | `/promotions/{promotion_id}/rules` | List rules |
| Orders | POST | `/orders/` | Create order and calculate total |
| Orders | GET | `/orders/` | List orders (optional `product_id`) |
| Orders | GET | `/orders/{order_id}` | Get one order |
| Pricing | POST | `/pricing/simulate` | Run and persist pricing decision |
| Analytics | GET | `/analytics/summary` | Dashboard KPI summary |
| Analytics | GET | `/analytics/decisions` | Pricing decision history |

## 3. Frontend connection examples

Use the backend base URL `http://127.0.0.1:8000/api`.

```js
const API = "http://127.0.0.1:8000/api";

// Create product — POST
const response = await fetch(`${API}/products/`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    id: "SKU-000001", name: "Laptop", category: "Electronics",
    brand: "Demo", unit: "each", min_price: 500,
    max_price: 2000, min_margin_pct: 15, is_active: true
  })
});
if (!response.ok) throw new Error((await response.json()).detail || "Create failed");
const createdProduct = await response.json();

// Add inventory — POST
await fetch(`${API}/inventory/`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ product_id: "SKU-000001", quantity_on_hand: 120, quantity_reserved: 8 })
});
```

Use `PATCH` for product/promotion edits and `DELETE` for removal. Keep `GET` for loading and refreshing lists. Do not call GET to create or update records.

## 4. Example request bodies

**Cost** `POST /api/costs/`

```json
{"product_id":"SKU-000001","unit_cost":420,"effective_from":"2026-11-01","effective_to":null}
```

**Competitor observation** `POST /api/competitors/`

```json
{"product_id":"SKU-000001","competitor_name":"Competitor A","observed_price":899,"source_url":"https://example.com/item","source_timestamp":"2026-11-13T10:00:00Z"}
```

**Promotion** `POST /api/promotions/`

```json
{"id":"PROMO-2026-000001","name":"Festival Offer","discount_type":"PERCENT","discount_value":10,"starts_at":"2026-11-13T00:00:00Z","ends_at":"2026-11-30T23:59:00Z","is_active":true}
```

**Order** `POST /api/orders/`

```json
{"product_id":"SKU-000001","quantity":2,"unit_price":899,"discount_amount":50}
```

**Pricing simulation** `POST /api/pricing/simulate`

```json
{"product_id":"SKU-000001","demand_index":1.2,"competitor_price":850,"competitor_age_hours":2,"apply_promotion_id":"PROMO-2026-000001"}
```

## 5. Authentication

Registration and login are implemented. Login returns `access_token` and `token_type`. For protected frontend calls, send:

```http
Authorization: Bearer <access_token>
```

The current business CRUD routes remain open for local demo integration; only `/api/auth/me` requires a token. Before deployment, apply `get_current_user` (and role checks) to business routes, set a strong `SECRET_KEY`, and configure allowed CORS origins.

## 6. Database

Default is SQLite at `backend/pricing_simulation.db` for simple local setup. Configure PostgreSQL by setting `DATABASE_URL` in `.env`, for example:

```env
DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/dynamic_pricing
SECRET_KEY=replace-with-a-long-random-secret
API_PREFIX=/api
```

The prototype creates tables on startup with SQLAlchemy `create_all`. Use Alembic migrations for production and when changing existing schemas. Back up the database before replacing the backend.

## 7. Tests

From `backend/` with the virtual environment activated:

```bash
pytest -q
```

The API tests exercise POST creation, GET retrieval, PATCH updates, DELETE, foreign-key parent validation, promotion rules, inventory validation, and order totals.

## 8. Important integration notes

- Create a product before adding its cost, inventory, competitor observations, or orders.
- Create an effective cost record and a price history record before running a pricing simulation. Use `POST /api/price-history/` to add the initial or later selling price.
- The simulation POST saves a `PriceDecision` record; retrieve it using `/api/analytics/decisions`.
- The current implementation is a local project starter, not a production deployment. Review authentication/authorization, migrations, audit logging, and promotion stacking before production use.
