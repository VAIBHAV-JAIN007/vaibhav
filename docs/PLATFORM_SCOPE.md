# Platform scope and delivery status

## Included in this repository
- Responsive static crypto dashboard using Binance public spot REST/WebSocket feeds.
- EMA, SMA, RSI, MACD and ATR indicators; rule-based signals and candle scanner.
- Risk sizing calculator.
- FastAPI backend with registration/login, JWT-protected portfolio and manual journal APIs.
- SQLAlchemy models and PostgreSQL Docker Compose setup.
- Market coverage endpoint that explicitly reports unsupported/licensed feeds.
- GitHub Actions Node.js checks and GitHub Pages static deployment workflow.

## Provider-dependent integrations (not live until configured)
- NSE/BSE cash, indices, futures, options chain, OI, PCR and Greeks.
- US and international equities.
- News and sentiment.
- Model-backed AI research.

These require authorized providers, credentials, and market-data redistribution rights where applicable. No synthetic prices are labelled live.

## Not yet production-deployed
- The API and database are source-configured for Docker but are not hosted by GitHub Pages.
- Production subscriptions, admin console, MFA, account recovery, alert delivery, audit pipeline and hosted backup/restore still need implementation and deployment.
- Broker order execution is intentionally excluded; users place trades manually.

## Before production use
Set strong secrets, HTTPS, restrictive CORS, rate limiting, email verification, MFA, audit logs, backups and monitoring. Add Alembic migrations before schema evolution. Review exchange/vendor terms and local compliance requirements.
