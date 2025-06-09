from typing import Optional

from pydantic import BaseModel, Field

class UserUpsetCommand(BaseModel):
    username: str
    sex: str
    age: int

class UserResponse(BaseModel):
    id: int
    username: str
    sex: str
    age: int

    class Config:
        from_attributes = True

class UserQuery(BaseModel):
    username: Optional[str] = Field(None, description="姓名模糊查询")
    sex: Optional[str] = Field(None, description="性别精确查询")
    age_min: Optional[int] = Field(None, ge=0, description="最小年龄")
    age_max: Optional[int] = Field(None, ge=0, description="最大年龄")
    order_by: str = Field("id", description="排序字段 (id/name/age)")
    desc: bool = Field(False, description="是否降序")



