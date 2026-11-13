import {useEffect,useState} from "react";
import {History,Search} from "lucide-react";
import DataTable from "../components/DataTable";
import {getDecisions} from "../services/api";
const money=n=>`₹${Number(n||0).toLocaleString("en-IN")}`;
export default function DecisionHistory(){
 const [rows,setRows]=useState([]);const [q,setQ]=useState("");useEffect(()=>{getDecisions().then(setRows)},[]);
 const filtered=rows.filter(r=>`${r.decision_code} ${r.sku} ${r.product_name} ${r.status}`.toLowerCase().includes(q.toLowerCase()));
 return <div className="page"><div className="page-heading"><div><div className="eyebrow">AUDIT TRAIL</div><h1>Decision history</h1><p>Trace previous pricing recommendations, outcomes and explanations.</p></div></div>
 <section className="panel"><div className="toolbar"><div className="search-field"><Search size={16}/><input value={q} onChange={e=>setQ(e.target.value)} placeholder="Search decision, SKU or status"/></div><span className="result-count"><History size={15}/> {filtered.length} decisions</span></div><DataTable columns={[{key:"decision_code",label:"Decision ID"},{key:"created_at",label:"Created at"},{key:"sku",label:"SKU"},{key:"product_name",label:"Product"},{key:"current_price",label:"Current price",render:money},{key:"recommended_price",label:"Recommended",render:v=>v?money(v):"—"},{key:"margin",label:"Margin",render:v=>`${v||0}%`},{key:"status",label:"Outcome",render:v=><span className={`status-badge ${String(v).toLowerCase()}`}>{v}</span>},{key:"reason",label:"Decision reason"}]} rows={filtered}/></section>
 </div>;
}