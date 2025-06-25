from fastapi_pagination import Page, Params
from fastapi_pagination.ext.tortoise import apaginate
from tortoise import transactions

from app.adapter.middleware.user_context import get_current_user
from app.application.schemas.user_schema import UserUpsetCommand, UserQuery
from app.domain.entity.user_entity import UserEntity
from app.domain.repository.user_repository import UserRepository
from app.infrastructure.persistence.models.user_model import UserModel


class UserRepositoryImpl(UserRepository):

    @transactions.atomic()
    async def create(self, user_upset_command: UserUpsetCommand) -> UserEntity:
        use_context = get_current_user()
        user_model = await UserModel.create(**user_upset_command.model_dump(), created_by=use_context.id, updated_by=use_context.id)
        return UserEntity(**user_model.model_to_dict())

    async def read(self, user_id: int) -> UserEntity | None:
        user_model = await UserModel.get_or_none(id=user_id)
        if user_model is None:
            return None
        return UserEntity(**user_model.model_to_dict())

    async def find(self, user_query: UserQuery, pagination: Params) -> Page[UserEntity]:
        query = UserModel.all()
        if user_query.username:
            query = query.filter(username__icontains=user_query.username)

        if user_query.gender:
            query = query.filter(gender=user_query.gender)

        if user_query.age_min is not None:
            query = query.filter(age__gte=user_query.age_min)
        if user_query.age_max is not None:
            query = query.filter(age__lte=user_query.age_max)

        order_prefix = "-" if user_query.desc else ""
        query = query.order_by(f"{order_prefix}{user_query.order_by}")

        raw_page = await apaginate(query, pagination)
        entity_items = [UserEntity(**item.model_dump()) for item in raw_page.items]

        return Page[UserEntity](
            items=entity_items,
            total=raw_page.total,
            page=raw_page.page,
            size=raw_page.size,
        )

    async def update(self, user_id: int, user_upset_command: UserUpsetCommand) -> UserEntity | None:
        # 使用in_transaction()实现事务
        async with transactions.in_transaction():
            try:
                use_context = get_current_user()
                await UserModel.filter(id=user_id).update(**user_upset_command.model_dump(exclude_unset=True), update_by=use_context.id)
                return await self.read(user_id)
                # 事务会自动提交（无异常时）
            except Exception as e:
                # 发生异常时自动回滚
                print("Transaction failed:", e)
                raise

    # 使用atomic()装饰器实现事务
    @transactions.atomic()
    async def delete(self, user_id: int) -> None:
        await UserModel.filter(id=user_id).delete()
