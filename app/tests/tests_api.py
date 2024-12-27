import pytest
import requests
from fastapi.testclient import TestClient
from ..main import app
from ..config import settings
from datetime import datetime

client = TestClient(app)

def test_create_transaction():
    headers = {"Authorization": f"ApiKey {settings.API_KEY}"}
    transaction_data = {
        "transaction_id": "test_transaction_123",
        "user_id": "user_001",
        "amount": 500.75,
        "currency": "USD",
        "timestamp": datetime.now().isoformat()
    }

    response = client.post("/transactions", json=transaction_data, headers=headers) 
    assert response.status_code == 200
    assert "message" in response.json()
    assert "task_id" in response.json()

def test_get_statistics():
    headers = {"Authorization": f"ApiKey {settings.API_KEY}"}
    response = client.get("/statistics", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "total_transactions" in data
    assert "average_transaction_amount" in data
    assert "top_transactions" in data
    
def test_delete_transaction():
    headers = {"Authorization": f"ApiKey {settings.API_KEY}"}
    response = client.delete("/transactions", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "All transactions deleted"

