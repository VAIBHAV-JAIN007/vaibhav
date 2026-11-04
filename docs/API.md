# API quick reference

Local base URL: http://localhost:8000. OpenAPI UI: /docs.

- GET /health — liveness check
- POST /api/v1/auth/register — create account (password minimum 12 characters)
- POST /api/v1/auth/login — obtain bearer token
- GET /api/v1/market/crypto/klines?symbol=BTCUSDT&interval=1h&limit=200 — Binance spot candles
- GET /api/v1/market/coverage — provider availability status
- GET/POST /api/v1/portfolio — JWT-protected manual positions
- GET/POST /api/v1/journal — JWT-protected trading journal

Send Authorization: Bearer <access_token> to protected endpoints. Replace the example JWT secret before deployment.
