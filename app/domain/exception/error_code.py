from enum import Enum

class ErrorCode(Enum):
    USER_NOT_FOUND = ("FASTAPI_0001", "用户[id={}]不存在")

    def __init__(self, code: str, description: str):
        self.code = code
        self.description = description