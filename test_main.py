import pytest
from fastapi.testclient import TestClient
from main import app

# Initialize the automated execution test client
client = TestClient(app)

def test_api_health_endpoint_returns_operational():
    """Validates the asynchronous core routing engine is online and responsive."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "operational", "engine": "Python 3.11/FastAPI"}

def test_register_batch_with_valid_compliance_payload():
    """Validates proper parsing and store mapping for regulatory compliance arrays."""
    valid_payload = {
        "batch_id": "BATCH-2026-99X",
        "component_code": "COMP-404",
        "quantity": 1500,
        "compliance_check": True
    }
    response = client.post("/api/v1/traceability/batch", json=valid_payload)
    assert response.status_code == 201
    assert response.json()["status"] == "success" or "securely indexed" in response.json()["message"]

def test_register_batch_fails_on_failed_compliance_check():
    """Verifies that the business logic correctly triggers a 400 Exception on failures."""
    invalid_payload = {
        "batch_id": "BATCH-FAIL-001",
        "component_code": "COMP-505",
        "quantity": 500,
        "compliance_check": False
    }
    response = client.post("/api/v1/traceability/batch", json=invalid_payload)
    assert response.status_code == 400
    assert "compliance" in response.json()["detail"].lower()
  
