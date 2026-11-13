import axios from "axios";

/*
  Set VITE_API_BASE_URL in frontend/.env.
  Example: VITE_API_BASE_URL=http://127.0.0.1:8000
  The API helpers return demo data if the backend is not reachable, so the
  interface can be developed independently. Set VITE_USE_MOCK_DATA=false
  to disable fallback data and see API errors instead.
*/
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api",
  timeout: 8000,
  headers: { "Content-Type": "application/json" }
});
const useMock = import.meta.env.VITE_USE_MOCK_DATA === "true";

const demo = {
  products: [
    { id: 1, sku: "SKU-000001", name: "Wireless Headphones", category: "Electronics", cost: 1450, current_price: 2299, floor_price: 1850, ceiling_price: 2799, min_margin: 18, status: "Active" },
    { id: 2, sku: "SKU-000002", name: "Smart Watch Series 4", category: "Electronics", cost: 2800, current_price: 3999, floor_price: 3500, ceiling_price: 4999, min_margin: 20, status: "Active" },
    { id: 3, sku: "SKU-000003", name: "Running Shoes", category: "Fashion", cost: 1100, current_price: 1899, floor_price: 1499, ceiling_price: 2299, min_margin: 15, status: "Active" },
    { id: 4, sku: "SKU-000004", name: "Coffee Maker", category: "Home", cost: 2100, current_price: 3199, floor_price: 2700, ceiling_price: 3999, min_margin: 18, status: "Active" },
    { id: 5, sku: "SKU-000005", name: "Bluetooth Speaker", category: "Electronics", cost: 850, current_price: 1399, floor_price: 1100, ceiling_price: 1799, min_margin: 16, status: "Review" }
  ],
  inventory: [
    { id: 1, sku: "SKU-000001", product_name: "Wireless Headphones", warehouse: "Vizag WH-01", available_stock: 142, reorder_level: 40, stock_status: "Healthy", updated_at: "2026-11-13" },
    { id: 2, sku: "SKU-000002", product_name: "Smart Watch Series 4", warehouse: "Hyderabad WH-02", available_stock: 24, reorder_level: 35, stock_status: "Low Stock", updated_at: "2026-11-13" },
    { id: 3, sku: "SKU-000003", product_name: "Running Shoes", warehouse: "Vizag WH-01", available_stock: 0, reorder_level: 25, stock_status: "Stockout", updated_at: "2026-11-13" },
    { id: 4, sku: "SKU-000004", product_name: "Coffee Maker", warehouse: "Chennai WH-03", available_stock: 68, reorder_level: 20, stock_status: "Healthy", updated_at: "2026-11-13" },
    { id: 5, sku: "SKU-000005", product_name: "Bluetooth Speaker", warehouse: "Vizag WH-01", available_stock: 18, reorder_level: 30, stock_status: "Low Stock", updated_at: "2026-11-13" }
  ],
  competitors: [
    { id: 1, sku: "SKU-000001", product_name: "Wireless Headphones", competitor: "MarketHub", observed_price: 2199, source_timestamp: "2026-11-13 10:15", freshness: "Fresh" },
    { id: 2, sku: "SKU-000002", product_name: "Smart Watch Series 4", competitor: "ShopKart", observed_price: 3799, source_timestamp: "2026-11-13 09:40", freshness: "Fresh" },
    { id: 3, sku: "SKU-000003", product_name: "Running Shoes", competitor: "MarketHub", observed_price: 1699, source_timestamp: "2026-11-10 11:00", freshness: "Stale" },
    { id: 4, sku: "SKU-000004", product_name: "Coffee Maker", competitor: "DealZone", observed_price: 3299, source_timestamp: "2026-11-13 08:25", freshness: "Fresh" }
  ],
  promotions: [
    { id: 1, code: "PROMO-2026-000001", name: "Festive Flash Sale", discount_type: "Percentage", discount_value: 10, start_date: "2026-11-10", end_date: "2026-11-20", status: "Active", stacking: "Not allowed" },
    { id: 2, code: "PROMO-2026-000002", name: "Electronics Cashback", discount_type: "Fixed", discount_value: 200, start_date: "2026-11-01", end_date: "2026-11-30", status: "Active", stacking: "Allowed" },
    { id: 3, code: "PROMO-2026-000003", name: "New Customer Offer", discount_type: "Percentage", discount_value: 5, start_date: "2026-11-15", end_date: "2026-11-30", status: "Scheduled", stacking: "Not allowed" }
  ],
  decisions: [
    { id: 1, decision_code: "DEC-2026-000001", sku: "SKU-000001", product_name: "Wireless Headphones", current_price: 2299, recommended_price: 2199, margin: 34.06, status: "Approved", reason: "Price aligned with fresh competitor observation while preserving margin." , created_at: "2026-11-13 10:30" },
    { id: 2, decision_code: "DEC-2026-000002", sku: "SKU-000002", product_name: "Smart Watch Series 4", current_price: 3999, recommended_price: 3899, margin: 28.19, status: "Approved", reason: "Moderate reduction recommended due to competitor pricing.", created_at: "2026-11-13 09:45" },
    { id: 3, decision_code: "DEC-2026-000003", sku: "SKU-000003", product_name: "Running Shoes", current_price: 1899, recommended_price: 0, margin: 0, status: "Blocked", reason: "Stockout detected. Price recommendation requires inventory review.", created_at: "2026-11-12 16:20" }
  ],
  analytics: { revenue: 1248500, revenue_change: 12.8, products: 5000, avg_margin: 26.4, alerts: 12, pricing_decisions: 846 }
};

async function requestOrDemo(request, fallback) {
  try { const response = await request(); return response.data; }
  catch (error) {
    if (useMock) return fallback;
    throw error;
  }
}
export const getProducts = () => requestOrDemo(() => api.get("/products/"), demo.products);
export const getInventory = () => requestOrDemo(() => api.get("/inventory/"), demo.inventory);
export const getCompetitors = () => requestOrDemo(() => api.get("/competitors/"), demo.competitors);
export const getPromotions = () => requestOrDemo(() => api.get("/promotions/"), demo.promotions);
export const getDecisions = () => requestOrDemo(() => api.get("/pricing/decisions"), demo.decisions);
export const getAnalytics = () => requestOrDemo(() => api.get("/analytics"), demo.analytics);
export const runPriceSimulation = (payload) =>
  requestOrDemo(() => api.post("/pricing/simulate", { product_id: payload.product_id,
    demand_index: payload.demand_index, competitor_price: payload.competitor_price || null,
    discount_percent: payload.discount_percent }), {
    current_price: Number(payload.current_price),
    recommended_price: Math.max(Number(payload.floor_price || 0), Math.min(Number(payload.ceiling_price || 999999), Number(payload.current_price) * (Number(payload.demand_index || 1) > 1.1 ? 1.03 : 0.97))),
    final_price: Math.max(Number(payload.floor_price || 0), Math.min(Number(payload.ceiling_price || 999999), Number(payload.current_price) * (Number(payload.demand_index || 1) > 1.1 ? 1.03 : 0.97))),
    margin: 0,
    status: "Demo result",
    reason: "Demo calculation only. Connect the backend pricing engine for authoritative decisions.",
    checks: { floor: true, ceiling: true, margin: true, stock: true, competitor_freshness: true, promotion: true }
  }).then(result => ({...result, margin: result.margin ?? result.margin_pct,
    recommended_price: result.recommended_price ?? result.final_price,
    checks: result.checks ?? {floor: true, ceiling: true, margin: (result.margin_pct ?? result.margin) >= (payload.min_margin || 0), stock: true, competitor_freshness: true, promotion: true}}));
export default api;
