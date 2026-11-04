# Global AI Trading Intelligence

Browser-based live crypto dashboard using Binance public REST and WebSocket market data.

## Deployment
Enable GitHub Pages with **Settings → Pages → Build and deployment → GitHub Actions**. The workflow deploys the repository root after each push to `main`. Check the Actions tab for the result and Pages URL.

## Current implemented scope
- Live Binance spot dashboard with candle chart and WebSocket updates
- Shared indicator library: EMA, SMA, RSI, MACD and ATR
- Rule-based signal classification with reasons and uncertainty labels
- Candle scanner for breakout, momentum and volume spikes
- Position sizing calculator with risk amount and risk/reward
- Automated Node.js smoke tests and syntax checks in GitHub Actions
- Binance spot ticker, candle history and WebSocket updates
- Price chart with EMA 9/21
- Browser-calculated RSI(14), MACD and ATR(14)
- Transparent rule-based BUY/SELL/HOLD educational signal
- Small market watch and local browser research notes

## Limitations
This is a starter crypto dashboard, not the complete global AI trading platform. It does not provide NSE/BSE or US equity feeds, options/OI/Greeks, news sentiment, a private AI model, backend, database, multi-user accounts, admin, subscriptions or broker execution. Real-time exchange data access and redistribution can require licensed providers. Signals are educational, not financial advice. Feed failure is reported, never replaced with invented prices.


Deployment check retriggered after Pages settings confirmation.

## Run checks in GitHub
Every push to `main` triggers `.github/workflows/ci.yml` (Node.js tests and syntax checks) and the Pages deployment workflow. Open the repository's **Actions** tab to inspect each run. GitHub Pages hosts the static frontend only; the API/backend and database are not deployed by this workflow.
