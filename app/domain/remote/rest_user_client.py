from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entity.user_entity import UserEntity

class RestUserClient(ABC):

    @abstractmethod
    async def get_user(self, user_id: int) -> Optional[UserEntity]:
        pass
