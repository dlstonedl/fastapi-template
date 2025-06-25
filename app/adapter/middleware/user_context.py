from contextvars import ContextVar
from dataclasses import dataclass
from typing import Optional

from app.domain.exception.base_exception import BusinessException
from app.domain.exception.error_code import ErrorCode


@dataclass
class UserContext:
    id: int
    username: str

current_user: ContextVar[Optional[UserContext]] = ContextVar("current_user", default=None)

def get_current_user() -> UserContext:
    user = current_user.get()
    if user is None:
        raise BusinessException(ErrorCode.USER_NOT_FOUND)
    return user



