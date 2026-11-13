export default function PriceComparison({current,competitor,recommended}) {
  const values=[{label:"Your price",value:Number(current||0),className:"price-current"},{label:"Competitor",value:Number(competitor||0),className:"price-competitor"},{label:"Recommended",value:Number(recommended||0),className:"price-recommended"}];
  const max=Math.max(...values.map(x=>x.value),1);
  return <div className="comparison-bars">{values.map(x=><div className="comparison-row" key={x.label}><div className="comparison-label"><span>{x.label}</span><strong>₹{x.value.toLocaleString("en-IN")}</strong></div><div className="bar-track"><div className={`bar-fill ${x.className}`} style={{width:`${x.value/max*100}%`}}/></div></div>)}</div>;
}