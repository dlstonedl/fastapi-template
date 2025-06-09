
from fastapi import APIRouter, HTTPException, Depends
from fastapi_pagination import Page, Params, add_pagination

from app.application.schemas.user_schema import UserUpsetCommand, UserResponse, UserQuery
from app.domain.repository.user_repository import UserRepository
from app.infrastructure.persistence.repository.user_repository_impl import UserRepositoryImpl

user_router = APIRouter()

repository_singleton = UserRepositoryImpl()

async def get_user_repository():
    return repository_singleton

@user_router.post("", response_model=UserResponse)
async def create(user_upset_command: UserUpsetCommand, user_repository: UserRepository = Depends(get_user_repository)):
    return await user_repository.create(user_upset_command)

@user_router.get("/{user_id}", response_model=UserResponse)
async def read(user_id: int, user_repository: UserRepository = Depends(get_user_repository)):
    if user := await user_repository.read(user_id):
        return user
    raise HTTPException(status_code=404, detail="User not found")

@user_router.get("", response_model=Page[UserResponse])
async def find(user_query: UserQuery = Depends(),
               pagination: Params = Depends(),
               user_repository: UserRepository = Depends(get_user_repository)):
    return await user_repository.find(user_query, pagination)

@user_router.put("/{user_id}", response_model=UserResponse)
async def update(user_id: int, user_upset_command: UserUpsetCommand, user_repository: UserRepository = Depends(get_user_repository)):
    if user := await user_repository.update(user_id, user_upset_command):
        return user
    raise HTTPException(status_code=404, detail="User not found")

@user_router.delete("/{user_id}")
async def delete(user_id: int, user_repository: UserRepository = Depends(get_user_repository)):
    await user_repository.delete(user_id)

add_pagination(user_router)