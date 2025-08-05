import pytest
from fastapi.testclient import TestClient
from tortoise import Tortoise

from app.main import app


@pytest.fixture(scope="session")
async def initialize_tests():
    """테스트용 데이터베이스 초기화"""
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={
            "models": [
                "app.models.user",
                "app.models.post",
                "app.models.comment",
                "app.models.profile",
            ]
        },
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()


@pytest.fixture
def client(initialize_tests):
    """FastAPI 테스트 클라이언트"""
    return TestClient(app)
