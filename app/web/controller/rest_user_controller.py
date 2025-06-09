
from fastapi import APIRouter, Depends

from app.domain.remote.rest_user_client import RestUserClient
from app.application.schemas.user_schema import UserResponse
from app.infrastructure.remote.rest_user_client_impl import RestUserClientImpl

rest_user_router = APIRouter()

async def get_rest_user_client():
    rest_user_client = RestUserClientImpl()
    try:
        yield rest_user_client
    finally:
        await rest_user_client.close()

@rest_user_router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, rest_user_client: RestUserClient = Depends(get_rest_user_client)):
    return await rest_user_client.get_user(user_id)

