from enum import Enum

class ErrorCode(Enum):
    USER_NOT_FOUND = ("FASTAPI_0001", "用户[id={}]不存在")
    USER_CONTEXT_NOT_SET = ("FASTAPI_0002", "用户上下文未设置")


    def __init__(self, code: str, description: str):
        self.code = code
        self.description = description