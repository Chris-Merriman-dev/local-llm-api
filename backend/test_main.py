from fastapi.testclient import TestClient
import pytest
from main import app

client = TestClient(app)

def test_get_history_endpoint():
    """Verify history endpoint returns a valid dictionary/list structure"""
    response = client.get("/get_history")
    assert response.status_code == 200
    assert "history" in response.json()

def test_stats_endpoint():
    """Verify system stats are reporting correctly"""
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert "cpu" in data
    assert "ram" in data
    # Verify uptime is a positive number
    assert data["uptime"] > 0

def test_cors_headers():
    """Ensure CORS is active for frontend communication"""
    response = client.options("/get_history", headers={
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "GET",
    })
    assert response.status_code == 200