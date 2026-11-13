import {useEffect,useState} from "react";
import {Calculator,ShieldCheck,AlertTriangle,Sparkles} from "lucide-react";
import {getProducts,runPriceSimulation} from "../services/api";
import PriceComparison from "../components/PriceComparison";
const money=n=>`₹${Number(n||0).toLocaleString("en-IN",{maximumFractionDigits:2})}`;
export default function PricingSimulator(){
 const [products,setProducts]=useState([]);const [productId,setProductId]=useState("");const [demand,setDemand]=useState("1.00");const [stock,setStock]=useState("100");const [competitor,setCompetitor]=useState("");const [discount,setDiscount]=useState("0");const [loading,setLoading]=useState(false);const [result,setResult]=useState(null);
 useEffect(()=>{getProducts().then(data=>{setProducts(data);if(data.length){setProductId(String(data[0].id));setCompetitor(String(data[0].current_price))}})},[]);
 const product=products.find(p=>String(p.id)===String(productId));
 useEffect(()=>{if(product){setCompetitor(String(product.current_price));setResult(null)}},[productId]);
 async function simulate(e){e.preventDefault();if(!product)return;setLoading(true);try{
  const payload={product_id:product.id,sku:product.sku,current_price:product.current_price,cost:product.cost,floor_price:product.floor_price,ceiling_price:product.ceiling_price,min_margin:product.min_margin,demand_index:Number(demand),available_stock:Number(stock),competitor_price:Number(competitor||0),discount_percent:Number(discount)};
  const res=await runPriceSimulation(payload);const finalPrice=Number(res.final_price??res.recommended_price??0);const margin=Number(res.margin??(finalPrice>0?(finalPrice*(1-Number(discount)/100)-product.cost)/(finalPrice*(1-Number(discount)/100))*100:0));
  setResult({...res,final_price:finalPrice,margin});
 }catch(err){alert(err.message||"Simulation failed")}finally{setLoading(false)}}
 return <div className="page"><div className="page-heading"><div><div className="eyebrow">DECISION ENGINE</div><h1>Pricing Simulator</h1><p>Test pricing scenarios against demand, stock, competitor and margin constraints.</p></div><span className="engine-pill"><span/> ENGINE READY</span></div>
 <div className="simulator-layout"><section className="panel simulator-form"><div className="panel-heading"><div><h2><Calculator size={18}/> Scenario inputs</h2><p>Choose a product and define market conditions.</p></div></div>
 <form onSubmit={simulate}>
  <label>Product / SKU<select required value={productId} onChange={e=>setProductId(e.target.value)}>{products.map(p=><option value={p.id} key={p.id}>{p.name} · {p.sku}</option>)}</select></label>
  {product&&<div className="product-context"><div><small>Current price</small><strong>{money(product.current_price)}</strong></div><div><small>Unit cost</small><strong>{money(product.cost)}</strong></div><div><small>Minimum margin</small><strong>{product.min_margin}%</strong></div></div>}
  <div className="form-grid"><label>Demand index<input type="number" min="0" max="5" step="0.01" value={demand} onChange={e=>setDemand(e.target.value)}/><small>1.00 = baseline demand</small></label><label>Available stock<input type="number" min="0" value={stock} onChange={e=>setStock(e.target.value)}/></label><label>Competitor price (₹)<input type="number" min="0" value={competitor} onChange={e=>setCompetitor(e.target.value)}/></label><label>Proposed discount (%)<input type="number" min="0" max="90" step="0.5" value={discount} onChange={e=>setDiscount(e.target.value)}/></label></div>
  {product&&<div className="guardrail-box"><div><ShieldCheck size={17}/><strong>Active price guardrails</strong></div><p>Floor: {money(product.floor_price)} <span/> Ceiling: {money(product.ceiling_price)}</p><p>Minimum margin: {product.min_margin}% · Discount evaluated before margin validation.</p></div>}
  <button className="primary-btn full-btn" type="submit" disabled={loading||!product}>{loading?"Calculating...":<><Sparkles size={17}/> Simulate pricing decision</>}</button>
 </form></section>
 <section className="panel result-panel"><div className="panel-heading"><div><h2>Simulation outcome</h2><p>Recommended action and validation results</p></div></div>
 {!result?<div className="empty-result"><div className="empty-icon"><Calculator size={25}/></div><strong>Ready to simulate</strong><p>Configure the scenario inputs and run the pricing engine to see its recommendation.</p></div>:<div className="result-content">
  <div className="recommendation-label">RECOMMENDED PRICE</div><div className="recommended-price">{money(result.final_price)}</div><span className={`status-badge ${String(result.status).toLowerCase().includes("block")?"blocked":"approved"}`}>{result.status||"Calculated"}</span>
  <div className="result-metrics"><div><small>Estimated margin</small><strong>{result.margin.toFixed(2)}%</strong></div><div><small>Current price</small><strong>{money(product?.current_price)}</strong></div></div>
  <PriceComparison current={product?.current_price} competitor={competitor} recommended={result.final_price}/>
  <div className="reason-box"><strong><AlertTriangle size={16}/> Decision explanation</strong><p>{result.reason||"Recommendation generated from the supplied scenario inputs."}</p></div>
  {result.checks&&<div className="check-list"><strong>Guardrail checks</strong>{Object.entries(result.checks).map(([k,v])=><div key={k}><span>{k.replaceAll("_"," ")}</span><b className={v?"check-pass":"check-fail"}>{v?"Passed":"Failed"}</b></div>)}</div>}
  <small className="disclaimer">A demo fallback is not an authoritative pricing decision. Persisted decisions and validation must come from the backend.</small>
 </div>}
 </section></div></div>;
}