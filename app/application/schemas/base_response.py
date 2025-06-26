from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar('T')

class BaseResponse(BaseModel, Generic[T]):
    code: str = "SUC0000"
    message: Optional[str] = None
    data: Optional[T] = None

    @classmethod
    def success(cls, data: T = None):
        return cls(data=data)

    @classmethod
    def error(cls, code: str, message: str = "error", data: T = None):
        return cls(code=code, message=message, data=data)