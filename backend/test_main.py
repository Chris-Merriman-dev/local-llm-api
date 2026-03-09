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
    """Verify system stats are reporting correctly"""
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert "cpu" in data
    assert "ram" in data
    assert data["uptime"] > 0

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