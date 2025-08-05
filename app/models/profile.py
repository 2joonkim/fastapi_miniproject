from tortoise.models import Model
from tortoise import fields

class Profile(Model):
    id = fields.IntField(pk=True)
    bio = fields.TextField(null=True)
    avatar_url = fields.CharField(max_length=500, null=True)
    birth_date = fields.DateField(null=True)
    
    # 일대일 관계
    user = fields.OneToOneField("models.User", related_name="profile")
    
    class Meta:
        table = "profiles"