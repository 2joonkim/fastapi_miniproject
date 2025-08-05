from tortoise.models import Model
from tortoise import fields

class Comment(Model):
    id = fields.IntField(pk=True)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    
    # 외래키 관계
    post = fields.ForeignKeyField("models.Post", related_name="comments")
    user = fields.ForeignKeyField("models.User", related_name="comments")
    
    class Meta:
        table = "comments"