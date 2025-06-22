from tortoise.models import Model
from tortoise import fields

class UserModel(Model):
    id = fields.IntField(primary_key=True)
    username = fields.CharField(max_length=100, description="姓名")
    sex = fields.CharField(max_length=10, description="性别")
    age = fields.IntField(description="年龄")

    class Meta:
        table = "user"
