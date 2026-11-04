import httpx
from fastapi import APIRouter, HTTPException, Query
from ..config import settings

router = APIRouter(prefix="/market", tags=["market-data"])
ALLOWED_INTERVALS = {"1m","3m","5m","15m","30m","1h","2h","4h","6h","8h","12h","1d","3d","1w","1M"}
YAHOO_RANGES = {"1d","5d","1mo","3mo","6mo","1y","2y","5y","10y","max"}
YAHOO_INTERVALS = {"1m","2m","5m","15m","30m","60m","90m","1h","1d","5d","1wk","1mo","3mo"}

async def yahoo_get(path: str, params: dict | None = None):
    url = "https://query1.finance.yahoo.com" + path
    headers = {"User-Agent": "Mozilla/5.0 GATI-MarketResearch/1.0"}
    try:
        async with httpx.AsyncClient(timeout=15, headers=headers, follow_redirects=True) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
    except (httpx.HTTPError, ValueError):
        raise HTTPException(status_code=502, detail="Market data source unavailable. No synthetic prices are returned.")

@router.get("/crypto/klines")
async def crypto_klines(symbol: str = Query("BTCUSDT", min_length=5, max_length=20), interval: str = "1h", limit: int = Query(200, ge=1, le=1000)):
    if interval not in ALLOWED_INTERVALS:
        raise HTTPException(status_code=422, detail="Unsupported candle interval")
    url = settings.binance_base_url.rstrip("/") + "/api/v3/klines"
    try:
        async with httpx.AsyncClient(timeout=12) as client:
            response = await client.get(url, params={"symbol": symbol.upper(), "interval": interval, "limit": limit})
            response.raise_for_status()
            rows = response.json()
        return {"provider":"Binance public spot API","market":"CRYPTO","symbol":symbol.upper(),"interval":interval,
                "data":[{"time":r[0],"open":float(r[1]),"high":float(r[2]),"low":float(r[3]),"close":float(r[4]),"volume":float(r[5])} for r in rows]}
    except (httpx.HTTPError, ValueError):
        raise HTTPException(status_code=502, detail="Market data provider unavailable; no synthetic prices are returned")

@router.get("/equities/chart")
async def equities_chart(
    symbol: str = Query(..., min_length=1, max_length=24),
    market: str = Query("US", pattern="^(US|NSE|BSE)$"),
    range: str = Query("1mo"),
    interval: str = Query("1d")
):
    if range not in YAHOO_RANGES or interval not in YAHOO_INTERVALS:
        raise HTTPException(status_code=422, detail="Unsupported range or candle interval")
    clean = symbol.strip().upper()
    if not clean.replace(".", "").replace("-", "").isalnum():
        raise HTTPException(status_code=422, detail="Invalid symbol")
    yahoo_symbol = clean if market == "US" else clean + (".NS" if market == "NSE" else ".BO")
    payload = await yahoo_get(f"/v8/finance/chart/{yahoo_symbol}", {"range": range, "interval": interval, "events": "div,splits"})
    result = (payload.get("chart") or {}).get("result") or []
    if not result:
        error = (payload.get("chart") or {}).get("error")
        raise HTTPException(status_code=404, detail=(error or {}).get("description", "Symbol not found or data unavailable"))
    item = result[0]
    quote = (item.get("indicators", {}).get("quote") or [{}])[0]
    timestamps = item.get("timestamp") or []
    candles = []
    for i, ts in enumerate(timestamps):
        values = [quote.get(k, []) for k in ("open","high","low","close","volume")]
        if all(i < len(v) and v[i] is not None for v in values[:4]):
            candles.append({"time": ts * 1000, "open": values[0][i], "high": values[1][i], "low": values[2][i], "close": values[3][i], "volume": values[4][i] if i < len(values[4]) else None})
    meta = item.get("meta", {})
    return {"provider":"Yahoo Finance public chart endpoint (unofficial; may be delayed)","market":market,"symbol":clean,"provider_symbol":yahoo_symbol,
            "currency":meta.get("currency"),"exchange":meta.get("exchangeName"),"timezone":meta.get("exchangeTimezoneName"),
            "regular_market_price":meta.get("regularMarketPrice"),"data_status":"may_be_delayed_unofficial_feed","data":candles}

@router.get("/options/{symbol}")
async def options_chain(symbol: str, expiration: int | None = None):
    clean = symbol.strip().upper()
    if not clean.replace(".", "").replace("-", "").isalnum():
        raise HTTPException(status_code=422, detail="Invalid symbol")
    params = {"date": expiration} if expiration else None
    payload = await yahoo_get(f"/v7/finance/options/{clean}", params)
    results = (payload.get("optionChain") or {}).get("result") or []
    if not results:
        raise HTTPException(status_code=404, detail="Options chain unavailable for this symbol from the current public source")
    item = results[0]
    return {"provider":"Yahoo Finance public options endpoint (unofficial; coverage varies)","symbol":clean,
            "underlying":item.get("quote",{}).get("regularMarketPrice"),"expiration_dates":item.get("expirationDates",[]),
            "options":item.get("options",[])}

@router.get("/coverage")
def coverage():
    return {
        "crypto":{"status":"connected-via-public-binance-adapter","coverage":"Binance spot pairs","note":"Public feed; provider terms apply"},
        "india_equities":{"status":"experimental_public_chart_adapter","markets":["NSE","BSE"],"endpoint":"/api/v1/market/equities/chart","note":"Yahoo Finance unofficial chart feed; may be delayed/incomplete; not exchange-authorized real-time data"},
        "us_equities":{"status":"experimental_public_chart_adapter","endpoint":"/api/v1/market/equities/chart","note":"Yahoo Finance unofficial chart feed; may be delayed/incomplete"},
        "options":{"status":"experimental_public_options_adapter","endpoint":"/api/v1/market/options/{symbol}","note":"Coverage varies; does not guarantee NSE/BSE index options, full Greeks, depth or real-time OI"},
        "news_sentiment":{"status":"provider_required","note":"Configure a licensed news/sentiment provider before enabling"},
        "market_depth":{"status":"provider_required","note":"Requires authorized exchange/brokerage data feed"}
    }
