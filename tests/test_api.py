from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "AI Personal OS Backend is running!"


def test_openapi_available():
    response = client.get("/openapi.json")
    assert response.status_code == 200
