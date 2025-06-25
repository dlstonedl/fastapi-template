from abc import ABC, abstractmethod

from fastapi_pagination import Params, Page

from app.application.schemas.user_schema import UserUpsetCommand, UserQuery
from app.domain.entity.user_entity import UserEntity

class UserRepository(ABC):

    @abstractmethod
    async def create(self, user_upset_command: UserUpsetCommand) -> UserEntity:
        pass

    @abstractmethod
    async def read(self, user_id: int) -> UserEntity | None:
        pass

    @abstractmethod
    async def find(self, user_query: UserQuery, pagination: Params) -> Page[UserEntity]:
        pass

    @abstractmethod
    async def update(self, user_id: int, user_upset_command: UserUpsetCommand) -> UserEntity | None:
        pass

    @abstractmethod
    async def delete(self, user_id: int) -> None:
        pass