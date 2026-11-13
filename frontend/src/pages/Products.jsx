import {useEffect,useMemo,useState} from "react";
import {Search,Plus,Download} from "lucide-react";
import DataTable from "../components/DataTable";
import {getProducts} from "../services/api";
const money=n=>`₹${Number(n||0).toLocaleString("en-IN")}`;
export default function Products(){
 const [rows,setRows]=useState([]);const [q,setQ]=useState("");
 useEffect(()=>{getProducts().then(setRows)},[]);
 const filtered=useMemo(()=>rows.filter(x=>`${x.sku} ${x.name} ${x.category}`.toLowerCase().includes(q.toLowerCase())),[rows,q]);
 return <div className="page"><div className="page-heading"><div><div className="eyebrow">CATALOGUE</div><h1>Products</h1><p>Manage product master data and pricing guardrails.</p></div><button className="secondary-btn" onClick={()=>alert("Connect product creation form to POST /products.")}><Plus size={16}/> Add product</button></div>
 <div className="panel"><div className="toolbar"><div className="search-field"><Search size={16}/><input value={q} onChange={e=>setQ(e.target.value)} placeholder="Search by SKU, product or category"/></div><button className="secondary-btn small" onClick={()=>window.print()}><Download size={15}/> Export</button><span className="result-count">{filtered.length} products</span></div>
 <DataTable columns={[{key:"sku",label:"SKU"},{key:"name",label:"Product name"},{key:"category",label:"Category"},{key:"cost",label:"Unit cost",render:v=>money(v)},{key:"current_price",label:"Current price",render:v=>money(v)},{key:"floor_price",label:"Price floor",render:v=>money(v)},{key:"ceiling_price",label:"Price ceiling",render:v=>money(v)},{key:"min_margin",label:"Min. margin",render:v=>`${v}%`},{key:"status",label:"Status",render:v=><span className="status-badge approved">{v}</span>}]} rows={filtered}/></div></div>;
}