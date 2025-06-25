
from fastapi import APIRouter, Depends

from app.application.schemas.base_response import BaseResponse
from app.domain.remote.rest_user_client import RestUserClient
from app.application.schemas.user_schema import UserResponse
from app.infrastructure.remote.rest_user_client_impl import RestUserClientImpl

router = APIRouter(prefix="/rest-users", tags=["远程用户"])

rest_user_client_singleton = RestUserClientImpl()

async def get_rest_user_client():
    return rest_user_client_singleton

@router.get("/{user_id}", response_model=BaseResponse[UserResponse])
async def get_user(user_id: int, rest_user_client: RestUserClient = Depends(get_rest_user_client)):
    user = await rest_user_client.get_user(user_id)
    return BaseResponse.success(user)

