from tortoise.models import Model
from tortoise import fields

class Post(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=200)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    # 외래키 관계
    user = fields.ForeignKeyField("models.User", related_name="posts")
    
    # 관계 설정
    comments: fields.ReverseRelation["Comment"]
    
    class Meta:
        table = "posts"