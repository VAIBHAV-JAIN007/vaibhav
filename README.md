# Global AI Trading Intelligence

Browser-based live crypto dashboard using Binance public REST and WebSocket market data.

## Deployment
Enable GitHub Pages with **Settings → Pages → Build and deployment → GitHub Actions**. The workflow deploys the repository root after each push to `main`. Check the Actions tab for the result and Pages URL.

## Current implemented scope
- Binance spot ticker, candle history and WebSocket updates
- Price chart with EMA 9/21
- Browser-calculated RSI(14), MACD and ATR(14)
- Transparent rule-based BUY/SELL/HOLD educational signal
- Small market watch and local browser research notes

## Limitations
This is a starter crypto dashboard, not the complete global AI trading platform. It does not provide NSE/BSE or US equity feeds, options/OI/Greeks, news sentiment, a private AI model, backend, database, multi-user accounts, admin, subscriptions or broker execution. Real-time exchange data access and redistribution can require licensed providers. Signals are educational, not financial advice. Feed failure is reported, never replaced with invented prices.
