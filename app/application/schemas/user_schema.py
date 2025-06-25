from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from app.domain.entity.gender import Gender


class UserUpsetCommand(BaseModel):
    username: str = Field(description="用户名")
    gender: Gender = Field(description="性别")
    age: int = Field(ge=0, description="年龄")

class UserResponse(BaseModel):
    id: int = Field(description="用户ID")
    username: str = Field(description="用户名")
    gender: Gender = Field(description="性别")
    age: int  = Field(description="年龄")
    created_at: datetime = Field(description="创建时间")
    updated_at: datetime = Field(description="更新时间")

    model_config = ConfigDict(
        from_attributes=True,
    )

class UserQuery(BaseModel):
    username: Optional[str] = Field(None, description="姓名模糊查询")
    gender: Optional[Gender] = Field(None, description="性别")
    age_min: Optional[int] = Field(None, ge=0, description="最小年龄")
    age_max: Optional[int] = Field(None, ge=0, description="最大年龄")
    order_by: str = Field("id", description="排序字段 (id/name/age)")
    desc: bool = Field(False, description="是否降序")



