# Global AI Trading Intelligence

Multi-market research terminal with a static browser frontend and a separately runnable FastAPI + PostgreSQL backend. No broker order execution.

## 1. Requirements

- Windows 10/11, macOS or Linux
- Git
- Docker Desktop with Docker Compose (recommended for the API/database)
- A modern browser
- Internet access for public market feeds

## 2. Download the complete source code

```bash
git clone https://github.com/VAIBHAV-JAIN007/vaibhav.git
cd vaibhav
```

Alternatively, use GitHub **Code → Download ZIP**, extract it, and open a terminal in the extracted folder.

## 3. Start the backend and PostgreSQL

### Windows PowerShell

```powershell
Copy-Item .env.example .env
notepad .env
```

Set strong private values in `.env` before use:

- `POSTGRES_PASSWORD`: a strong database password
- `JWT_SECRET`: a long random secret (32+ random bytes)
- `CORS_ORIGINS`: keep `http://localhost:8080` for local frontend access

Then run:

```powershell
docker compose up --build -d
docker compose ps
```

### macOS / Linux

```bash
cp .env.example .env
# Edit .env and set strong POSTGRES_PASSWORD and JWT_SECRET values
docker compose up --build -d
docker compose ps
```

Verify:
- API health: http://localhost:8000/health
- Interactive API docs: http://localhost:8000/docs
- Market coverage: http://localhost:8000/api/v1/market/coverage

Stop services with `docker compose down`. Keep database data with the named Docker volume. To stop and delete the database volume, use `docker compose down -v` (destructive).

## 4. Start the frontend

Keep the backend running. Open a second terminal in the project root.

### Windows

```powershell
py -m http.server 8080
```

### macOS / Linux

```bash
python3 -m http.server 8080
```

Open http://localhost:8080. Backend API URL should be `http://localhost:8000`.

Do not open `index.html` directly as a `file://` URL; use the local web server.

## 5. Market support and honest limitations

| Market / feature | Current implementation | Important limitation |
|---|---|---|
| Crypto spot | Binance public REST + WebSocket | Spot pairs only; provider/network availability applies |
| NSE equities | Yahoo public chart adapter via backend | Unofficial, may be delayed/incomplete; not exchange-authorized real-time |
| BSE equities | Yahoo public chart adapter via backend | Unofficial, may be delayed/incomplete |
| US equities | Yahoo public chart adapter via backend | Unofficial, may be delayed/incomplete |
| Options | Experimental Yahoo public options endpoint | Coverage varies; not a complete Indian index options feed |
| RSI, EMA, MACD, ATR | Local calculations on loaded candles | Research indicators, not predictive guarantees |
| Scanner | Breakout, momentum and volume checks | Based on loaded candles only |
| Position sizing | Risk and reward calculator | User-entered assumptions |
| Watchlist / journal | Browser localStorage | Stored only in this browser |
| Login / portfolio API | FastAPI auth and account routers | Run backend; configure secure production deployment |
| Market depth / order book | Not enabled | Requires authorized exchange/broker data |
| News / sentiment / AI model | Not enabled | Requires a selected model and data provider |
| Alerts / backtesting / subscription billing | Not production-ready | Additional implementation and hosting required |

### Live market data

This repository does **not** claim full exchange-real-time coverage. For production-grade NSE/BSE cash, indices, futures/options, OI, PCR, Greeks and depth, obtain exchange-authorized data or a licensed distributor entitlement. US real-time quotes/depth also require the appropriate market-data entitlements. Add provider credentials as server-side deployment secrets only; never commit API keys or put them in browser JavaScript.

The experimental Yahoo adapter can be rate-limited, blocked, delayed or return no data. The UI should show an error rather than invent a quote.

## 6. Run tests

Install Node.js 20+ and Python 3.11+ if you want to run the checks locally.

Frontend:
```bash
npm test
npm run check
```

Backend:
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r backend/requirements.txt
cd backend
pytest
```

GitHub Actions also runs frontend and backend tests on pushes.

## 7. Deploying

GitHub Pages can host only the static frontend. The FastAPI API and PostgreSQL database must run on a separate server/hosting provider with HTTPS, persistent storage, backups, environment secrets, monitoring and appropriate access controls. Set the frontend API URL to the deployed HTTPS API URL and configure that exact frontend origin in backend CORS settings.

No direct broker order placement is included. This is a research and decision-support tool, not financial advice.
