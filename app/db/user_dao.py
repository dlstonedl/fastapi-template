from fastapi_pagination import Page, Params
from fastapi_pagination.ext.tortoise import apaginate

from app.models.user import User
from app.schemas.user import UserIn, UserQueryParam


async def create_user(user_in: UserIn) -> User:
    return await User.create(**user_in.model_dump())

async def read_user(user_id: int) -> User | None:
    return await User.get_or_none(id=user_id)


async def find_user(user_query: UserQueryParam, pagination: Params) -> Page[User]:
    query = User.all()
    if user_query.username:
        query = query.filter(username__icontains=user_query.username)

    if user_query.sex:
        query = query.filter(sex=user_query.sex)

    if user_query.age_min is not None:
        query = query.filter(age__gte=user_query.age_min)
    if user_query.age_max is not None:
        query = query.filter(age__lte=user_query.age_max)

    order_prefix = "-" if user_query.desc else ""
    query = query.order_by(f"{order_prefix}{user_query.order_by}")

    return await apaginate(query, pagination)

async def update_user(user_id: int, user_in: UserIn) -> User | None:
    await User.filter(id=user_id).update(**user_in.model_dump(exclude_unset=True))
    return await User.get_or_none(id=user_id)

async def delete_user(user_id: int) -> None:
    await User.filter(id=user_id).delete()

