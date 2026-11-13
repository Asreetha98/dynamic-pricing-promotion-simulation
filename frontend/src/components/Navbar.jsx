import { Bell, Search, CircleUserRound } from "lucide-react";
export default function Navbar() {
  return <header className="topbar">
    <div className="mobile-brand">PricePilot</div>
    <div className="search-wrap"><Search size={17}/><input placeholder="Search SKU, product or decision..." /></div>
    <div className="topbar-right"><span className="today-label">Friday, 13 November 2026</span><button className="icon-button" aria-label="Notifications"><Bell size={19}/><i/></button><div className="user-chip"><div className="avatar">OP</div><div><strong>Operator</strong><small>Admin workspace</small></div><CircleUserRound size={18}/></div></div>
  </header>;
}