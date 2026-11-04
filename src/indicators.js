// Pure technical indicators. Input candles: {open, high, low, close, volume}.
const closesOf = candles => candles.map(c => Number(c.close));
export function ema(values, period) {
  if (!Array.isArray(values) || period < 1 || values.length < period) return [];
  const k=2/(period+1), out=Array(period-1).fill(null);
  let prev=values.slice(0,period).reduce((a,b)=>a+Number(b),0)/period;
  out.push(prev);
  for(let i=period;i<values.length;i++){prev=Number(values[i])*k+prev*(1-k);out.push(prev);}
  return out;
}
export function sma(values, period) {
  return values.map((_,i)=>i+1<period?null:values.slice(i+1-period,i+1).reduce((a,b)=>a+Number(b),0)/period);
}
export function rsi(values, period=14) {
  if(values.length<=period)return [];
  let gain=0,loss=0;
  for(let i=1;i<=period;i++){const d=values[i]-values[i-1];gain+=Math.max(d,0);loss+=Math.max(-d,0);}
  let ag=gain/period,al=loss/period,out=Array(period).fill(null);
  const calc=()=>al===0?100:100-100/(1+ag/al);
  out.push(calc());
  for(let i=period+1;i<values.length;i++){const d=values[i]-values[i-1];ag=(ag*(period-1)+Math.max(d,0))/period;al=(al*(period-1)+Math.max(-d,0))/period;out.push(calc());}
  return out;
}
export function macd(values,fast=12,slow=26,signal=9){
  const f=ema(values,fast),s=ema(values,slow),line=values.map((_,i)=>f[i]==null||s[i]==null?null:f[i]-s[i]);
  const valid=line.filter(v=>v!=null),sigValid=ema(valid,signal),sig=Array(line.length-valid.length).fill(null).concat(sigValid);
  return {line,signal:sig,histogram:line.map((v,i)=>v==null||sig[i]==null?null:v-sig[i])};
}
export function atr(candles,period=14){
  if(candles.length<=period)return [];
  const tr=candles.map((c,i)=>i===0?Number(c.high)-Number(c.low):Math.max(Number(c.high)-Number(c.low),Math.abs(Number(c.high)-Number(candles[i-1].close)),Math.abs(Number(c.low)-Number(candles[i-1].close))));
  const out=Array(period).fill(null);let value=tr.slice(1,period+1).reduce((a,b)=>a+b,0)/period;out.push(value);
  for(let i=period+1;i<tr.length;i++){value=(value*(period-1)+tr[i])/period;out.push(value);}return out;
}
export function calculateIndicators(candles){
 const c=closesOf(candles),m=macd(c);
 return {ema9:ema(c,9),ema21:ema(c,21),sma50:sma(c,50),rsi14:rsi(c),macd:m,atr14:atr(candles)};
}
