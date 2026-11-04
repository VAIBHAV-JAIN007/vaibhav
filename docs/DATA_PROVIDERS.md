# Market data provider integration

The current backend adapter retrieves public Binance spot candles. It is not an exchange-authorized global market terminal.

Add separate authorized adapters for:
- India: NSE/BSE authorized distributor for cash, indices, derivatives and options chain.
- US/international: licensed equities market-data provider.
- News: API with appropriate usage and redistribution rights.
- Options: timestamped chain, OI, volume and Greeks (or required calculation inputs).

Normalize provider, exchange, symbol, instrument type, timestamp, currency, price, volume and realtime/delayed status. Never mix delayed and realtime data in the UI. Store API keys in deployment secrets, never browser code or Git.
