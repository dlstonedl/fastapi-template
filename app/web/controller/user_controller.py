
from fastapi import APIRouter, HTTPException, Depends
from fastapi_pagination import Page, Params, add_pagination

from app.application.schemas.user_schema import UserUpsetCommand, UserResponse, UserQuery
from app.infrastructure.persistence.dao.user_dao import create_user, read_user, update_user, delete_user, find_user

user_router = APIRouter()

@user_router.post("", response_model=UserResponse)
async def create(user_upset_command: UserUpsetCommand):
    return await create_user(user_upset_command)

@user_router.get("/{user_id}", response_model=UserResponse)
async def read(user_id: int):
    if user := await read_user(user_id):
        return user
    raise HTTPException(status_code=404, detail="User not found")

@user_router.get("", response_model=Page[UserResponse])
async def find(user_query: UserQuery = Depends(), pagination: Params = Depends()):
    return await find_user(user_query, pagination)

@user_router.put("/{user_id}", response_model=UserResponse)
async def update(user_id: int, user_upset_command: UserUpsetCommand):
    if user := await update_user(user_id, user_upset_command):
        return user
    raise HTTPException(status_code=404, detail="User not found")

@user_router.delete("/{user_id}")
async def delete(user_id: int):
    await delete_user(user_id)

add_pagination(user_router)