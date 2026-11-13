# PricePilot – Dynamic Pricing & Promotion Simulation Frontend

React + Vite frontend for the Dynamic Pricing and Promotion Simulation System.

## 1. Requirements
- Node.js 18 or newer
- npm
- Backend API (FastAPI) when integrating live data

## 2. Run the frontend
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```
Open http://localhost:5173

## 3. Backend connection
The frontend expects the FastAPI server at `http://127.0.0.1:8000/api` by default.
Change `VITE_API_BASE_URL` in `.env` if your backend uses another URL.

Current API calls in `src/services/api.js`:
| Frontend helper | Method and endpoint |
|---|---|
| getProducts | GET /products |
| getInventory | GET /inventory |
| getCompetitors | GET /competitors |
| getPromotions | GET /promotions |
| getDecisions | GET /pricing/decisions |
| getAnalytics | GET /analytics |
| runPriceSimulation | POST /pricing/simulate |

These are the frontend's expected route contracts. If the actual FastAPI routes or field names differ, update only `src/services/api.js` and the simulator payload mapping.

## 4. Demo data mode
`VITE_USE_MOCK_DATA=true` enables local demo data when the backend is unavailable. This is useful while building frontend and backend separately.
Set `VITE_USE_MOCK_DATA=false` to surface API errors instead of falling back to demo data.
Demo fallback simulation is illustrative and is not the authoritative business pricing engine.

## 5. Important business rule
The final margin must be calculated after discount:
`margin % = (discounted selling price - unit cost) / discounted selling price * 100`
The backend should enforce price floor, ceiling, minimum margin, promotion stacking/exclusion, inventory and competitor freshness rules. Frontend validation is not a replacement for backend validation.

## 6. Suggested integration order
1. Confirm FastAPI route names and response field names.
2. Connect products and inventory.
3. Connect competitor observations and promotions.
4. Connect `/pricing/simulate`.
5. Connect persisted decision history and analytics.
