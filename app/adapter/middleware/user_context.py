from contextvars import ContextVar
from dataclasses import dataclass
from typing import Optional

@dataclass
class UserContext:
    id: int
    username: str

current_user: ContextVar[Optional[UserContext]] = ContextVar("current_user", default=None)


