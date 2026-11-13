import { useEffect,useState } from "react";
import { IndianRupee, Package, Percent, AlertTriangle, ArrowUpRight, ArrowRight, Activity } from "lucide-react";
import { Link } from "react-router-dom";
import { AreaChart,Area,ResponsiveContainer,CartesianGrid,XAxis,YAxis,Tooltip,BarChart,Bar } from "recharts";
import StatCard from "../components/StatCard";
import DataTable from "../components/DataTable";
import {getAnalytics,getDecisions,getInventory} from "../services/api";

const trend=[{day:"Mon",sales:72,margin:24},{day:"Tue",sales:88,margin:26},{day:"Wed",sales:78,margin:25},{day:"Thu",sales:105,margin:27},{day:"Fri",sales:96,margin:26},{day:"Sat",sales:122,margin:29},{day:"Sun",sales:114,margin:28}];
const money=n=>`₹${Number(n||0).toLocaleString("en-IN")}`;
export default function Dashboard(){
 const [stats,setStats]=useState({}); const [decisions,setDecisions]=useState([]); const [inventory,setInventory]=useState([]);
 useEffect(()=>{getAnalytics().then(setStats);getDecisions().then(setDecisions);getInventory().then(setInventory)},[]);
 const alerts=inventory.filter(x=>["Low Stock","Stockout"].includes(x.stock_status));
 return <div className="page">
  <div className="page-heading"><div><div className="eyebrow">OVERVIEW</div><h1>Good afternoon, Operator</h1><p>Here is what is happening across your pricing operations today.</p></div><Link className="primary-btn" to="/simulator"><Activity size={17}/> Run simulation</Link></div>
  <div className="stat-grid">
   <StatCard label="Tracked products" value={Number(stats.products||5000).toLocaleString("en-IN")} change="+4.6%" note="vs. previous month" icon={Package} tone="blue"/>
   <StatCard label="Revenue tracked" value={money(stats.revenue||1248500)} change="+12.8%" note="vs. previous period" icon={IndianRupee} tone="green"/>
   <StatCard label="Average margin" value={`${stats.avg_margin||26.4}%`} change="+2.1%" note="portfolio average" icon={Percent} tone="purple"/>
   <StatCard label="Open exceptions" value={stats.alerts||12} change="Needs attention" note="pricing & inventory alerts" icon={AlertTriangle} tone="orange"/>
  </div>
  <div className="dashboard-grid">
   <section className="panel chart-panel"><div className="panel-heading"><div><h2>Sales & margin trend</h2><p>Performance over the last 7 days</p></div><span className="select-pill">Last 7 days⌄</span></div><div className="chart-legend"><span><i className="legend-dot blue-dot"/> Sales index</span><span><i className="legend-dot green-dot"/> Margin %</span></div><div className="chart-area"><ResponsiveContainer width="100%" height="100%"><AreaChart data={trend}><defs><linearGradient id="salesFill" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#5278ee" stopOpacity={0.22}/><stop offset="100%" stopColor="#5278ee" stopOpacity={0}/></linearGradient></defs><CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#edf0f5"/><XAxis dataKey="day" axisLine={false} tickLine={false}/><YAxis axisLine={false} tickLine={false}/><Tooltip/><Area type="monotone" dataKey="sales" stroke="#5278ee" strokeWidth={2.5} fill="url(#salesFill)"/><Area type="monotone" dataKey="margin" stroke="#19a77a" strokeWidth={2.5} fill="none"/></AreaChart></ResponsiveContainer></div></section>
   <section className="panel"><div className="panel-heading"><div><h2>Operational health</h2><p>Current exception overview</p></div><span className="live-pill"><i/> LIVE</span></div><div className="health-score"><div className="health-ring"><strong>94</strong><small>/100</small></div><div><strong>Healthy operations</strong><p>Most pricing guardrails are operating within limits.</p></div></div><div className="health-list"><div><span className="health-indicator green-bg"/>Pricing guardrails<span className="right-value">Passed</span></div><div><span className="health-indicator green-bg"/>Data synchronization<span className="right-value">Active</span></div><div><span className="health-indicator orange-bg"/>Inventory exceptions<span className="right-value">{alerts.length} items</span></div></div><Link to="/reports" className="text-link">View system report <ArrowRight size={15}/></Link></section>
  </div>
  <section className="panel table-panel"><div className="panel-heading"><div><h2>Recent pricing decisions</h2><p>Latest recommendations from the pricing engine</p></div><Link to="/decisions" className="text-link">View all <ArrowUpRight size={15}/></Link></div><DataTable columns={[{key:"decision_code",label:"Decision ID"},{key:"product_name",label:"Product"},{key:"current_price",label:"Current price",render:v=>money(v)},{key:"recommended_price",label:"Recommended",render:v=>v?money(v):"—"},{key:"margin",label:"Margin",render:v=>`${v||0}%`},{key:"status",label:"Status",render:v=><span className={`status-badge ${String(v).toLowerCase()}`}>{v}</span>}]} rows={decisions.slice(0,4)}/></section>
 </div>;
}