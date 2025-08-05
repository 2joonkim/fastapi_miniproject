from tortoise import Tortoise

from app.core.config import settings

# Tortoise ORM 설정
TORTOISE_ORM = {
    "connections": {"default": settings.database_url},
    "apps": {
        "models": {
            "models": [
                "app.models.user",
                "app.models.post",
                "app.models.comment",
                "app.models.profile",
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
}


async def init_db():
    """데이터베이스 초기화"""
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()


async def close_db():
    """데이터베이스 연결 종료"""
    await Tortoise.close_connections()
