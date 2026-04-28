import pytest
import pytest_asyncio
from faker import Faker
from httpx import ASGITransport, AsyncClient

from app.main import app


pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


def make_user_payload(faker: Faker, age: int | None = None) -> dict:
    return {
        "username": faker.user_name(),
        "age": faker.random_int(min=0, max=90) if age is None else age,
    }


async def test_create_user_returns_201_and_response_shape(async_client: AsyncClient, faker: Faker):
    payload = make_user_payload(faker)

    response = await async_client.post("/users", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["username"] == payload["username"]
    assert body["age"] == payload["age"]


async def test_get_existing_user_returns_200(async_client: AsyncClient, faker: Faker):
    payload = make_user_payload(faker)
    create_response = await async_client.post("/users", json=payload)
    user_id = create_response.json()["id"]

    response = await async_client.get(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.json() == {"id": user_id, **payload}


async def test_get_missing_user_returns_404(async_client: AsyncClient):
    response = await async_client.get("/users/999")

    assert response.status_code == 404
    assert response.json()["message"] == "User not found"


async def test_delete_existing_user_returns_204(async_client: AsyncClient, faker: Faker):
    payload = make_user_payload(faker)
    create_response = await async_client.post("/users", json=payload)
    user_id = create_response.json()["id"]

    response = await async_client.delete(f"/users/{user_id}")

    assert response.status_code == 204
    assert response.content == b""


async def test_repeated_delete_returns_404(async_client: AsyncClient, faker: Faker):
    payload = make_user_payload(faker)
    create_response = await async_client.post("/users", json=payload)
    user_id = create_response.json()["id"]

    first_delete = await async_client.delete(f"/users/{user_id}")
    second_delete = await async_client.delete(f"/users/{user_id}")

    assert first_delete.status_code == 204
    assert second_delete.status_code == 404
    assert second_delete.json()["message"] == "User not found"


async def test_create_user_accepts_boundary_age(async_client: AsyncClient, faker: Faker):
    payload = make_user_payload(faker, age=0)

    response = await async_client.post("/users", json=payload)

    assert response.status_code == 201
    assert response.json()["age"] == 0


async def test_create_user_rejects_invalid_age(async_client: AsyncClient, faker: Faker):
    payload = make_user_payload(faker, age=-1)

    response = await async_client.post("/users", json=payload)

    assert response.status_code == 422
    assert response.json()["error_code"] == "validation_error"

