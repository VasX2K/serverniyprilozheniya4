from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_custom_exception_a_response():
    response = client.get("/demo-errors/a")

    assert response.status_code == 400
    assert response.json() == {
        "error_code": "custom_exception_a",
        "message": "Business rule failed for demo endpoint A",
        "details": [],
    }


def test_custom_exception_b_response():
    response = client.get("/demo-errors/b")

    assert response.status_code == 404
    assert response.json() == {
        "error_code": "custom_exception_b",
        "message": "Demo resource was not found",
        "details": [],
    }


def test_validate_user_success():
    response = client.post(
        "/validate-user",
        json={
            "username": "student",
            "age": 20,
            "email": "student@example.com",
            "password": "password1",
            "phone": "+79990000000",
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "User data is valid"


def test_validate_user_custom_validation_error():
    response = client.post(
        "/validate-user",
        json={
            "username": "student",
            "age": 18,
            "email": "not-an-email",
            "password": "short",
        },
    )

    body = response.json()
    assert response.status_code == 422
    assert body["error_code"] == "validation_error"
    assert body["message"] == "Request validation failed"
    assert {detail["location"] for detail in body["details"]} >= {
        "body.age",
        "body.email",
        "body.password",
    }

