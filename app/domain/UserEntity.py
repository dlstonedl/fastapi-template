from dataclasses import dataclass

@dataclass
class UserEntity:
    id: int
    username: str
    sex: str
    age: int
