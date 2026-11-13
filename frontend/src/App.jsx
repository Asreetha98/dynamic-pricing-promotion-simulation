import { Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";
import Products from "./pages/Products";
import Inventory from "./pages/Inventory";
import Competitors from "./pages/Competitors";
import Promotions from "./pages/Promotions";
import PricingSimulator from "./pages/PricingSimulator";
import DecisionHistory from "./pages/DecisionHistory";
import Reports from "./pages/Reports";

export default function App() {
  return <div className="app-shell">
    <Sidebar />
    <div className="main-area">
      <Navbar />
      <main className="page-container">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/products" element={<Products />} />
          <Route path="/inventory" element={<Inventory />} />
          <Route path="/competitors" element={<Competitors />} />
          <Route path="/promotions" element={<Promotions />} />
          <Route path="/simulator" element={<PricingSimulator />} />
          <Route path="/decisions" element={<DecisionHistory />} />
          <Route path="/reports" element={<Reports />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  </div>;
}