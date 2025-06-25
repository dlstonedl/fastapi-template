from types import NoneType
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Body
from fastapi_pagination import Page, Params, add_pagination

from app.application.schemas.base_response import BaseResponse
from app.application.schemas.user_schema import UserUpsetCommand, UserResponse, UserQuery
from app.domain.exception.base_exception import BusinessException
from app.domain.exception.error_code import ErrorCode
from app.domain.repository.user_repository import UserRepository
from app.infrastructure.persistence.repository.user_repository_impl import UserRepositoryImpl

router = APIRouter(prefix="/users", tags=["用户"])

repository_singleton = UserRepositoryImpl()

async def get_user_repository():
    return repository_singleton

@router.post("", response_model=BaseResponse[UserResponse])
async def create(user_upset_command: UserUpsetCommand, user_repository: UserRepository = Depends(get_user_repository)):
    user_response = await user_repository.create(user_upset_command)
    return BaseResponse.success(user_response)

@router.get("/{user_id}", response_model=BaseResponse[UserResponse])
async def read(user_id: Annotated[int, Path(description="用户ID")],
               user_repository: Annotated[UserRepository, Depends(get_user_repository)]):
    if user := await user_repository.read(user_id):
        return BaseResponse.success(user)
    raise BusinessException(ErrorCode.USER_NOT_FOUND, user_id)

@router.get("", response_model=BaseResponse[Page[UserResponse]])
async def find(user_query: Annotated[UserQuery, Depends()],
               pagination: Annotated[Params, Depends()],
               user_repository: Annotated[UserRepository, Depends(get_user_repository)]):
    user_page = await user_repository.find(user_query, pagination)
    return BaseResponse.success(user_page)

@router.put("/{user_id}", response_model=BaseResponse[UserResponse])
async def update(user_id: int = Path(..., description="用户ID"),
                 user_upset_command: UserUpsetCommand = Body(...),
                 user_repository: UserRepository = Depends(get_user_repository)):
    if user := await user_repository.update(user_id, user_upset_command):
        return BaseResponse.success(user)
    raise BusinessException(ErrorCode.USER_NOT_FOUND, user_id)

@router.delete("/{user_id}", response_model=BaseResponse[NoneType])
async def delete(user_id: int = Path(..., description="用户ID"),
                 user_repository: UserRepository = Depends(get_user_repository)):
    await user_repository.delete(user_id)
    return BaseResponse.success()

add_pagination(router)