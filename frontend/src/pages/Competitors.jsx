import {useEffect,useState} from "react";
import {Radar,Clock3,AlertTriangle} from "lucide-react";
import DataTable from "../components/DataTable";
import {getCompetitors,getProducts} from "../services/api";
const money=n=>`₹${Number(n||0).toLocaleString("en-IN")}`;
export default function Competitors(){
 const [rows,setRows]=useState([]);const [products,setProducts]=useState([]);
 useEffect(()=>{getCompetitors().then(setRows);getProducts().then(setProducts)},[]);
 const enriched=rows.map(r=>({...r,our_price:products.find(p=>p.sku===r.sku)?.current_price}));
 return <div className="page"><div className="page-heading"><div><div className="eyebrow">MARKET INTELLIGENCE</div><h1>Competitor observations</h1><p>Compare observed market prices and identify stale competitor data.</p></div><button className="secondary-btn" onClick={()=>alert("Connect observation ingestion to POST /competitors.")}><Radar size={16}/> Add observation</button></div>
 <div className="notice"><Clock3 size={18}/><div><strong>Observation freshness matters</strong><p>Stale competitor observations should not be treated as current inputs in pricing decisions.</p></div></div>
 <section className="panel"><div className="panel-heading"><div><h2>Latest competitor prices</h2><p>Source timestamps are retained for traceability.</p></div></div><DataTable columns={[{key:"sku",label:"SKU"},{key:"product_name",label:"Product"},{key:"competitor",label:"Competitor"},{key:"our_price",label:"Our price",render:v=>money(v)},{key:"observed_price",label:"Observed price",render:v=>money(v)},{key:"source_timestamp",label:"Source timestamp"},{key:"freshness",label:"Freshness",render:v=><span className={`status-badge ${v==="Fresh"?"approved":"warning"}`}>{v==="Stale"&&<AlertTriangle size={12}/>} {v}</span>}]} rows={enriched}/></section>
 </div>;
}