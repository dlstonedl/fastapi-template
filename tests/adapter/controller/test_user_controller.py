import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient
from tortoise import Tortoise

from app.adapter.controller.user_controller import router

@pytest.fixture(scope="session", autouse=True)
def init_tortoise():
    import asyncio

    async def init():
        await Tortoise.init(
            db_url="sqlite://:memory:",
            modules={"models": ["app.infrastructure.persistence.models.user_model"]},
        )
        await Tortoise.generate_schemas()

    asyncio.run(init())
    yield
    asyncio.run(Tortoise.close_connections())

@pytest.fixture(scope="session")
def app():
    app = FastAPI()
    app.include_router(router)
    return app

@pytest.fixture
def client(app):
    return TestClient(app)

def test_create_user(client):
    # given
    user_data = {"username": "test", "sex": "male", "age": 30}

    # when
    response = client.post("/users", json=user_data)

    # then
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "test"
    assert data["sex"] == "male"
    assert data["age"] == 30