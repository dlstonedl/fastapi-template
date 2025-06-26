import json
from dataclasses import asdict
from datetime import datetime
from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from app.adapter.controller.user_controller import router, get_user_repository
from app.domain.entity.gender import Gender
from app.domain.entity.user_entity import UserEntity
from tests.adapter.controller.json_encode import EnhancedJSONEncoder


@pytest.fixture
def mock_repo():
    repo = AsyncMock()
    return repo

@pytest.fixture
def client(mock_repo):
    app = FastAPI()
    app.include_router(router)

    async def override_get_user_repository():
        return mock_repo

    app.dependency_overrides[get_user_repository] = override_get_user_repository

    return TestClient(app)


def test_create_user(client, mock_repo):
    # given
    user_data = {"username": "test", "gender": "MALE", "age": 30}
    user_entity = UserEntity(id=1, username="test", gender=Gender.MALE, age=30,
                             created_at=datetime.fromisoformat("2025-06-25T00:00:00"),
                             updated_at=datetime.fromisoformat("2025-06-25T00:00:00"),
                             created_by="system", updated_by="system")
    mock_repo.create.return_value = user_entity

    # when
    response = client.post("/users", json=user_data)

    # then
    assert response.status_code == 200

    assert response.json()['data'] == json.loads(json.dumps(asdict(user_entity), cls=EnhancedJSONEncoder))

def test_read_user(client, mock_repo):
    # given
    user_entity = UserEntity(id=1, username="test", gender=Gender.MALE, age=30,
                             created_at=datetime.fromisoformat("2025-06-25T00:00:00"),
                             updated_at=datetime.fromisoformat("2025-06-25T00:00:00"),
                             created_by="system", updated_by="system")
    mock_repo.read.return_value = user_entity

    # when
    response = client.get("/users/1")

    # then
    assert response.status_code == 200
    assert response.json()['data'] == json.loads(json.dumps(asdict(user_entity), cls=EnhancedJSONEncoder))





