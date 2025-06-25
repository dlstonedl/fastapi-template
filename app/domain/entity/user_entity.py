from dataclasses import dataclass
from datetime import datetime

from app.domain.entity.gender import Gender


@dataclass
class UserEntity:
    id: int
    username: str
    gender: Gender
    age: int
    created_at: datetime
    updated_at: datetime



