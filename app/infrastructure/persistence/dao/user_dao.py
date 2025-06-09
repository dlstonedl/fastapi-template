from fastapi_pagination import Page, Params
from fastapi_pagination.ext.tortoise import apaginate

from app.application.schemas.user_schema import UserUpsetCommand, UserQuery
from app.infrastructure.persistence.models.user_model import UserModel
from tortoise import transactions

@transactions.atomic()
async def create_user(user_upset_command: UserUpsetCommand) -> UserModel:
    return await UserModel.create(**user_upset_command.model_dump())

async def read_user(user_id: int) -> UserModel | None:
    return await UserModel.get_or_none(id=user_id)


async def find_user(user_query: UserQuery, pagination: Params) -> Page[UserModel]:
    query = UserModel.all()
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

async def update_user(user_id: int, user_upset_command: UserUpsetCommand) -> UserModel | None:
    # 使用in_transaction()实现事务
    async with transactions.in_transaction():
        try:
            await UserModel.filter(id=user_id).update(**user_upset_command.model_dump(exclude_unset=True))
            return await UserModel.get_or_none(id=user_id)
            # 事务会自动提交（无异常时）
        except Exception as e:
            # 发生异常时自动回滚
            print("Transaction failed:", e)
            raise

# 使用atomic()装饰器实现事务
@transactions.atomic()
async def delete_user(user_id: int) -> None:
    await UserModel.filter(id=user_id).delete()
