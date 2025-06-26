from dataclasses import asdict
from datetime import datetime

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient
from tortoise import Tortoise

from app.adapter.controller.user_controller import router
from app.adapter.middleware.auth_middleware import auth_middleware
from app.domain.entity.gender import Gender
from app.domain.entity.user_entity import UserEntity
from app.infrastructure.persistence.models.user_model import UserModel


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
    app.middleware("http")(auth_middleware)
    return app

@pytest.fixture
def client(app):
    return TestClient(app)

def test_create_user(client):
    # given
    user_data = {"username": "test", "gender": "MALE", "age": 30}

    # when
    headers = {"Authorization": "Bearer 100:system"}
    response = client.post("/users", json=user_data, headers=headers)

    # then
    assert response.status_code == 200
    data = response.json()['data']
    assert data["username"] == "test"
    assert data["gender"] == "MALE"
    assert data["age"] == 30


def test_read_user(client):
    # given
    user_entity = UserEntity(id=3, username="test", gender=Gender.MALE, age=30,
                             created_at=datetime.fromisoformat("2025-06-25T00:00:00"),
                             updated_at=datetime.fromisoformat("2025-06-25T00:00:00"),
                             created_by="system", updated_by="system")
    import asyncio
    asyncio.run(UserModel.create(**asdict(user_entity)))

    # when
    response = client.get("/users/3")

    # then
    assert response.status_code == 200
    data = response.json()['data']
    assert data["username"] == "test"
    assert data["gender"] == "MALE"
    assert data["age"] == 30
