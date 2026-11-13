import {useEffect,useState} from "react";
import {BadgePercent,Plus} from "lucide-react";
import DataTable from "../components/DataTable";
import {getPromotions} from "../services/api";
export default function Promotions(){
 const [rows,setRows]=useState([]);useEffect(()=>{getPromotions().then(setRows)},[]);
 return <div className="page"><div className="page-heading"><div><div className="eyebrow">CAMPAIGN MANAGEMENT</div><h1>Promotions</h1><p>Review promotion periods, discount values and stacking restrictions.</p></div><button className="secondary-btn" onClick={()=>alert("Connect promotion creation to POST /promotions.")}><Plus size={16}/> Create promotion</button></div>
 <div className="notice purple-notice"><BadgePercent size={18}/><div><strong>Promotion rule validation</strong><p>Eligibility, exclusions and stacking rules must be validated before a discount is applied.</p></div></div>
 <section className="panel"><div className="panel-heading"><div><h2>Promotion register</h2><p>Configured promotions and lifecycle status</p></div><span className="select-pill">All statuses⌄</span></div><DataTable columns={[{key:"code",label:"Promotion ID"},{key:"name",label:"Promotion"},{key:"discount_type",label:"Discount type"},{key:"discount_value",label:"Discount",render:(v,r)=>r.discount_type==="Percentage"?`${v}%`:`₹${v}`},{key:"start_date",label:"Start date"},{key:"end_date",label:"End date"},{key:"stacking",label:"Stacking rule"},{key:"status",label:"Status",render:v=><span className={`status-badge ${v==="Active"?"approved":"warning"}`}>{v}</span>}]} rows={rows}/></section>
 </div>;
}