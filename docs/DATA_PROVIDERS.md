# Market data provider integration

## Available adapters in this repository

- **Crypto spot:** Binance public REST candles and WebSocket dashboard feed. Public feed terms and regional availability apply.
- **NSE/BSE equities:** `GET /api/v1/market/equities/chart?market=NSE&symbol=RELIANCE` or `market=BSE`. This uses Yahoo Finance's public chart endpoint (for example, `.NS` / `.BO` symbols). It is unofficial, may be delayed, incomplete or unavailable, and is not an exchange-authorized real-time feed.
- **US equities:** the same endpoint with `market=US&symbol=AAPL`. Also unofficial and potentially delayed.
- **Options (experimental):** `GET /api/v1/market/options/{symbol}` uses a public Yahoo endpoint. Coverage varies; it does not guarantee Indian index options, complete OI, Greeks, depth or real-time data.
- **Market depth / order book:** not enabled; requires an authorized provider.
- **News and sentiment:** not enabled; requires a news API with appropriate usage and redistribution rights.

## API examples

```text
GET /api/v1/market/coverage
GET /api/v1/market/equities/chart?market=NSE&symbol=RELIANCE&range=1mo&interval=1d
GET /api/v1/market/equities/chart?market=BSE&symbol=500325&range=3mo&interval=1d
GET /api/v1/market/equities/chart?market=US&symbol=MSFT&range=1mo&interval=1d
GET /api/v1/market/options/AAPL
```

## Production requirements for full exchange coverage

For dependable live NSE/BSE cash, indices, futures/options, market depth and OI, procure an exchange-authorized data feed or licensed distributor. For US real-time quotes/depth, procure a suitable consolidated/exchange data entitlement. Configure credentials as server-side deployment secrets; never put provider keys in browser JavaScript or Git.

Normalize provider, exchange, symbol, instrument type, timestamp, currency, price, volume and real-time/delayed status. Never mix delayed and real-time data in the UI. Display provider and last-updated time on every instrument. Add rate limits, caching, entitlement checks and provider-failure handling before production use.

No broker order execution is included. Research signals are not financial advice.
