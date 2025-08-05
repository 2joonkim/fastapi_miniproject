from typing import TYPE_CHECKING

from tortoise import fields
from tortoise.models import Model

if TYPE_CHECKING:
    from .post import Post
    from .profile import Profile


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    email = fields.CharField(max_length=100, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    # 관계 설정 (N+1 문제 해결을 위해)
    posts: fields.ReverseRelation["Post"]
    profile: fields.ReverseRelation["Profile"]

    class Meta:
        table = "users"
