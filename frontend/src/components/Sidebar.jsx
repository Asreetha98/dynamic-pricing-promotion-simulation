import { NavLink } from "react-router-dom";
import { LayoutDashboard, Package, Warehouse, Tags, BadgePercent, SlidersHorizontal, History, ChartNoAxesCombined, Activity } from "lucide-react";
const links = [
  {to:"/",label:"Dashboard",icon:LayoutDashboard},
  {to:"/products",label:"Products",icon:Package},
  {to:"/inventory",label:"Inventory",icon:Warehouse},
  {to:"/competitors",label:"Competitors",icon:Tags},
  {to:"/promotions",label:"Promotions",icon:BadgePercent},
  {to:"/simulator",label:"Pricing Simulator",icon:SlidersHorizontal},
  {to:"/decisions",label:"Decision History",icon:History},
  {to:"/reports",label:"Reports",icon:ChartNoAxesCombined}
];
export default function Sidebar() {
  return <aside className="sidebar">
    <div className="brand"><div className="brand-mark"><Activity size={21}/></div><div><strong>PricePilot</strong><small>PRICING INTELLIGENCE</small></div></div>
    <div className="workspace-label">WORKSPACE</div>
    <nav>{links.map(({to,label,icon:Icon})=><NavLink key={to} to={to} end={to==="/"} className={({isActive})=>isActive?"nav-link active":"nav-link"}><Icon size={18}/><span>{label}</span>{label==="Pricing Simulator"&&<span className="nav-tag">CORE</span>}</NavLink>)}</nav>
    <div className="sidebar-bottom"><div className="system-status"><span className="status-dot"/> System operational</div><small>Dynamic Pricing Engine · v1.0</small></div>
  </aside>;
}