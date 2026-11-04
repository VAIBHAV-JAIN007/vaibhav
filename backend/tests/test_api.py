from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_coverage_reports_actual_provider_limits():
    data = client.get("/api/v1/market/coverage").json()
    assert data["crypto"]["status"] == "connected-via-public-binance-adapter"
    assert data["india_equities"]["status"] == "experimental_public_chart_adapter"
    assert data["us_equities"]["status"] == "experimental_public_chart_adapter"
    assert data["options"]["status"] == "experimental_public_options_adapter"
    assert data["market_depth"]["status"] == "provider_required"

def test_equity_chart_rejects_invalid_market():
    response = client.get("/api/v1/market/equities/chart", params={"symbol":"RELIANCE","market":"INVALID"})
    assert response.status_code == 422

def test_equity_chart_rejects_invalid_range():
    response = client.get("/api/v1/market/equities/chart", params={"symbol":"AAPL","market":"US","range":"bad"})
    assert response.status_code == 422
