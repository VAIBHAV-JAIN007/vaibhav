# Global AI Trading Intelligence

A responsive trading research platform with a browser dashboard and a separately runnable FastAPI + PostgreSQL backend.

## Start the complete local stack
1. Install Docker Desktop.
2. In the repository folder, copy `.env.example` to `.env`.
3. Replace `POSTGRES_PASSWORD` and `JWT_SECRET` with strong random values.
4. Run `docker compose up --build`.
5. Open API docs at http://localhost:8000/docs and health at http://localhost:8000/health.
6. Open `index.html` using a local static web server (for example, `python -m http.server 8080`) and visit http://localhost:8080. GitHub Pages deploys the static frontend automatically when Pages is enabled.

## Included
- Binance spot price/candles and WebSocket dashboard.
- EMA/SMA/RSI/MACD/ATR analysis, rule-based signal explanations and candle scanner.
- Position risk calculator.
- FastAPI registration/login, JWT-protected manual portfolio and trading journal.
- SQLAlchemy data models, PostgreSQL and Docker Compose.
- Market coverage endpoint with explicit provider availability status.
- GitHub Actions tests for frontend and backend.

## Data and deployment limitations
NSE/BSE, US equities, options chain/OI/PCR/Greeks, news sentiment and model-backed AI require suitable providers, credentials and possibly redistribution licences. They are not represented as live until configured. GitHub Pages hosts only static frontend files; the API and database run separately through Docker or a hosting provider. No broker order execution is included.

See [platform scope](docs/PLATFORM_SCOPE.md), [API guide](docs/API.md) and [data provider guide](docs/DATA_PROVIDERS.md).
