
from fastapi import APIRouter, HTTPException, Depends, Path, Body
from fastapi_pagination import Page, Params, add_pagination

from app.application.schemas.user_schema import UserUpsetCommand, UserResponse, UserQuery
from app.domain.repository.user_repository import UserRepository
from app.infrastructure.persistence.repository.user_repository_impl import UserRepositoryImpl

router = APIRouter(prefix="/users", tags=["用户"])

repository_singleton = UserRepositoryImpl()

async def get_user_repository():
    return repository_singleton

@router.post("", response_model=UserResponse)
async def create(user_upset_command: UserUpsetCommand, user_repository: UserRepository = Depends(get_user_repository)):
    return await user_repository.create(user_upset_command)

@router.get("/{user_id}", response_model=UserResponse)
async def read(user_id: int = Path(..., description="用户ID"),
               user_repository: UserRepository = Depends(get_user_repository)):
    if user := await user_repository.read(user_id):
        return user
    raise HTTPException(status_code=404, detail="User not found")

@router.get("", response_model=Page[UserResponse])
async def find(user_query: UserQuery = Depends(),
               pagination: Params = Depends(),
               user_repository: UserRepository = Depends(get_user_repository)):
    return await user_repository.find(user_query, pagination)

@router.put("/{user_id}", response_model=UserResponse)
async def update(user_id: int = Path(..., description="用户ID"),
                 user_upset_command: UserUpsetCommand = Body(...),
                 user_repository: UserRepository = Depends(get_user_repository)):
    if user := await user_repository.update(user_id, user_upset_command):
        return user
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/{user_id}")
async def delete(user_id: int = Path(..., description="用户ID"),
                 user_repository: UserRepository = Depends(get_user_repository)):
    await user_repository.delete(user_id)

add_pagination(router)