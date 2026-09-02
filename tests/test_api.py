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


def test_tasks_endpoint():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_assignments_endpoint():
    response = client.get("/assignments")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_timetable_endpoint():
    response = client.get("/timetable")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
