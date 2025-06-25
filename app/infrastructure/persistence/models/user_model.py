from typing import Any

from tortoise.models import Model
from tortoise import fields

from app.domain.entity.gender import Gender


class UserModel(Model):
    id = fields.IntField(primary_key=True)
    username = fields.CharField(max_length=100, description="姓名")
    gender = fields.CharEnumField(enum_type=Gender, max_length=10, description="性别")
    age = fields.IntField(description="年龄")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    created_by = fields.CharField(max_length=20, description="创建人")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")
    updated_by = fields.CharField(max_length=20, description="更新人")


    class Meta:
        table = "user"

    def model_to_dict(self) -> dict[str, Any]:
        data = vars(self)
        return {key : value for key, value in data.items() if not key.startswith('_')}

