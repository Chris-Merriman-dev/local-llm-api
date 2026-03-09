from fastapi.testclient import TestClient
import pytest
from unittest.mock import patch
from main import app

client = TestClient(app)

def test_get_history_endpoint():
    """Verify history endpoint returns a valid dictionary/list structure"""
    response = client.get("/get_history")
    assert response.status_code == 200
    assert "history" in response.json()

def test_stats_endpoint():
    """Verify all 7 system metrics are reporting correctly"""
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()

    # 1. Verify all expected keys exist in the response
    expected_keys = ["cpu", "ram", "disk", "net_down", "net_up", "processes", "uptime"]
    for key in expected_keys:
        assert key in data

    # 2. Logic/Sanity Checks
    assert data["uptime"] > 0
    assert data["processes"] > 0  # There should always be at least one process running (the server itself!)
    
    # 3. Percentage Checks (Optional but smart)
    # CPU, RAM, and Disk should be between 0 and 100
    assert 0 <= data["cpu"] <= 100
    assert 0 <= data["ram"] <= 100
    assert 0 <= data["disk"] <= 100

def test_ask_sentinel_endpoint_mocked():
    """Verify API logic without needing a local Ollama instance"""
    
    # Target the method we just looked at
    target = 'main.model_engine.ask_model_with_chat_history'
    
    with patch(target) as mocked_ask:
        # We mimic your return: (ai_reply, chat_history)
        mocked_ask.return_value = (
            "This is a fake AI response.", 
            [
                {"role": "user", "content": "Hello"}, 
                {"role": "assistant", "content": "This is a fake AI response."}
            ]
        )

        payload = {"messages": [{"role": "user", "content": "Hello"}]}
        response = client.post("/ask_sentinel", json=payload)

        assert response.status_code == 200
        assert response.json()["reply"] == "This is a fake AI response."
        mocked_ask.assert_called_once()

def test_cors_headers():
    """Ensure CORS is active for frontend communication"""
    response = client.options("/get_history", headers={
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "GET",
    })
    assert response.status_code == 200