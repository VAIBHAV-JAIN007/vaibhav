from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_coverage_is_transparent():
    data = client.get("/api/v1/market/coverage").json()
    assert data["india_equities"]["status"] == "provider_required"
    assert data["us_equities"]["status"] == "provider_required"
