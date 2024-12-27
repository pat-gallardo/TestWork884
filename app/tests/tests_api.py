import pytest
import requests
from fastapi.testclient import TestClient
from ..main import app
from ..config import settings
from datetime import datetime

client = TestClient(app)

def test_create_transaction():
    print("\n====================== CREATE TRANSACTION ======================")
    headers = {"Authorization": f"ApiKey {settings.API_KEY}"}
    transaction_data = {
        "transaction_id": "test_transaction_123",
        "user_id": "user_001",
        "amount": 500.75,
        "currency": "USD",
        "timestamp": datetime.now().isoformat()
    }

    response = client.post("/transactions", json=transaction_data, headers=headers) 
    if response.status_code != 200:
        print("Create Transaction Error:", response.json())
        return
    assert response.status_code == 200
    print("status_code: ", response.status_code)
    assert "message" in response.json()
    print("message: ", response.json().get("message"))
    assert "task_id" in response.json()
    print("task_id: ", response.json().get("task_id"))
    

def test_get_statistics():
    print("====================== GET STATISTICS ======================")
    headers = {"Authorization": f"ApiKey {settings.API_KEY}"}
    response = client.get("/statistics", headers=headers)
    if response.status_code != 200:
        print("Get Statistics Error:", response.json())
        return
    assert response.status_code == 200
    print("status_code: ", response.status_code)
    data = response.json()
    assert "total_transactions" in data
    print("total_transactions: ", data.get("total_transactions"))
    assert "average_transaction_amount" in data
    print("average_transaction_amount: ",data.get("average_transaction_amount"))
    assert "top_transactions" in data
    print("top_transactions: ", data.get("top_transactions"))
    
def test_delete_transaction():
    print("====================== DELETE TRANSACTION ======================")
    headers = {"Authorization": f"ApiKey {settings.API_KEY}"}
    response = client.delete("/transactions", headers=headers)
    if response.status_code != 200:
        print("Delete Transaction Error:", response.json())
        return
    assert response.status_code == 200
    print("status_code: ", response.status_code)
    assert response.json()["message"] == "All transactions deleted"
    print("message: ", response.json().get("message"))

