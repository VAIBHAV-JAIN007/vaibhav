import {ema,rsi} from "./indicators.js";
export function scanCandles(candles){
 const closes=candles.map(c=>Number(c.close)),volumes=candles.map(c=>Number(c.volume||0));
 if(candles.length<30)return {status:"INSUFFICIENT_DATA",setups:[]};
 const e20=ema(closes,20),e50=ema(closes,50),r=rsi(closes,14),i=closes.length-1;
 const avgVol=volumes.slice(-21,-1).reduce((a,b)=>a+b,0)/20;
 const currentVol=volumes[i],priorHigh=Math.max(...candles.slice(-21,-1).map(c=>Number(c.high)));
 const setups=[];
 if(closes[i]>priorHigh&&currentVol>avgVol*1.5)setups.push({type:"BREAKOUT",label:"20-candle high breakout",volumeRatio:avgVol?currentVol/avgVol:null});
 if(e20[i]>e50[i]&&closes[i]>e20[i]&&r[i]>=55)setups.push({type:"MOMENTUM",label:"EMA trend with RSI strength",rsi:r[i]});
 if(avgVol>0&&currentVol>avgVol*2)setups.push({type:"VOLUME_SPIKE",label:"Volume above 2x average",volumeRatio:currentVol/avgVol});
 return {status:"OK",setups};
}
