from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_app_loads():
    response = client.get("/")
    assert response.status_code in (200, 404)


def test_openapi_available():
    response = client.get("/openapi.json")
    assert response.status_code == 200
