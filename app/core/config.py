import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 앱 기본 설정
    app_name: str = "FastAPI Mini Project"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000

    # PostgreSQL 데이터베이스 설정
    pg_name: str = "framework_project"
    pg_user: str = "user"
    pg_password: str = "password"
    pg_host: str = "localhost"
    pg_port: int = 5432
    database_url: str = "sqlite://db.sqlite3"

    # 보안 설정
    secret_key: str = "dev-secret-key"
    cors_origins: list[str] = ["http://localhost:3000"]

    # 로깅 설정
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = False


# 환경에 따른 설정 파일 선택
def get_settings() -> Settings:
    env = os.getenv("ENVIRONMENT", "development")
    if env == "production":
        return Settings(_env_file=".env.prod")
    return Settings(_env_file=".env")


settings = get_settings()
