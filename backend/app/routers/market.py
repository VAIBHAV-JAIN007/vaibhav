import httpx
from fastapi import APIRouter, HTTPException, Query
from ..config import settings

router = APIRouter(prefix="/market", tags=["market-data"])
ALLOWED_INTERVALS = {"1m","3m","5m","15m","30m","1h","2h","4h","6h","8h","12h","1d","3d","1w","1M"}

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

@router.get("/coverage")
def coverage():
    return {"crypto":{"status":"connected-via-public-binance-adapter","note":"Spot data only; provider terms apply"},
            "india_equities":{"status":"provider_required","markets":["NSE","BSE"]},
            "us_equities":{"status":"provider_required"},
            "options":{"status":"provider_required","fields":["chain","open_interest","PCR","Greeks"]},
            "news_sentiment":{"status":"provider_required"}}
