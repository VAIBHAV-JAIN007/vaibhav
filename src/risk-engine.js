// Position sizing and risk/reward helpers. Monetary values use the same currency.
export function riskPlan({capital,riskPercent,entry,stop,target}){
  for(const [k,v] of Object.entries({capital,riskPercent,entry,stop,target})) if(!Number.isFinite(Number(v))||Number(v)<=0) throw new Error(k+" must be greater than zero");
  const direction=Number(target)>Number(entry)?"LONG":Number(target)<Number(entry)?"SHORT":"INVALID";
  if(direction==="INVALID"||(direction==="LONG"&&Number(stop)>=Number(entry))||(direction==="SHORT"&&Number(stop)<=Number(entry))) throw new Error("Stop and target are inconsistent with trade direction");
  const riskPerUnit=Math.abs(Number(entry)-Number(stop)),rewardPerUnit=Math.abs(Number(target)-Number(entry));
  const riskAmount=Number(capital)*Number(riskPercent)/100;
  return {direction,riskAmount,riskPerUnit,rewardPerUnit,quantity:Math.floor(riskAmount/riskPerUnit),riskReward:rewardPerUnit/riskPerUnit};
}
export function classifySignal({price,emaFast,emaSlow,rsiValue,macdHistogram}){
  const values=[price,emaFast,emaSlow,rsiValue,macdHistogram];
  if(values.some(v=>v==null||!Number.isFinite(Number(v)))) return {action:"WAIT",score:0,confidence:"LOW",reasons:["Insufficient indicator history"]};
  let score=0,reasons=[];
  if(price>emaFast){score++;reasons.push("Price above fast EMA");}else{score--;reasons.push("Price below fast EMA");}
  if(emaFast>emaSlow){score++;reasons.push("Fast EMA above slow EMA");}else{score--;reasons.push("Fast EMA below slow EMA");}
  if(rsiValue>=50&&rsiValue<=70){score++;reasons.push("RSI has positive momentum");}else if(rsiValue<45){score--;reasons.push("RSI momentum is weak");}
  if(macdHistogram>0){score++;reasons.push("MACD histogram positive");}else{score--;reasons.push("MACD histogram negative");}
  const action=score>=3?"BUY":score<=-3?"SELL":"HOLD";
  return {action,score,confidence:Math.abs(score)>=4?"MEDIUM":"LOW",reasons};
}
