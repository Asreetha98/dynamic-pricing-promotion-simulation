import {useEffect,useState} from "react";
import {Warehouse,AlertTriangle,PackageCheck} from "lucide-react";
import StatCard from "../components/StatCard";
import DataTable from "../components/DataTable";
import {getInventory} from "../services/api";
export default function Inventory(){
 const [rows,setRows]=useState([]);useEffect(()=>{getInventory().then(setRows)},[]);
 const low=rows.filter(x=>x.stock_status==="Low Stock").length,zero=rows.filter(x=>x.stock_status==="Stockout").length;
 return <div className="page"><div className="page-heading"><div><div className="eyebrow">SUPPLY & AVAILABILITY</div><h1>Inventory</h1><p>Monitor stock positions that influence pricing and promotion decisions.</p></div></div>
 <div className="stat-grid three"><StatCard label="Tracked SKUs" value={rows.length||"—"} note="inventory records" icon={Warehouse}/><StatCard label="Low stock" value={low} note="Below reorder level" icon={AlertTriangle} tone="orange"/><StatCard label="Stockouts" value={zero} note="No available units" icon={PackageCheck} tone="purple"/></div>
 <section className="panel"><div className="panel-heading"><div><h2>Inventory snapshot</h2><p>Latest available stock by warehouse</p></div><span className="select-pill">All warehouses⌄</span></div><DataTable columns={[{key:"sku",label:"SKU"},{key:"product_name",label:"Product"},{key:"warehouse",label:"Warehouse"},{key:"available_stock",label:"Available stock"},{key:"reorder_level",label:"Reorder level"},{key:"stock_status",label:"Stock status",render:v=><span className={`status-badge ${v==="Healthy"?"approved":v==="Stockout"?"blocked":"warning"}`}>{v}</span>},{key:"updated_at",label:"Last updated"}]} rows={rows}/></section>
 </div>;
}