import os
from functools import lru_cache
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class ConfigMixin:
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


class PostgresSettings(BaseSettings, ConfigMixin):
    host: str | None = os.getenv("POSTGRES_HOST")
    port: str | None = os.getenv("POSTGRES_PORT")
    db: str | None = os.getenv("POSTGRES_DB")
    user: str | None = os.getenv("POSTGRES_USER")
    password: str | None = os.getenv("POSTGRES_PASSWORD")

    @property
    def postgres_dsn(self) -> PostgresDsn:
        return PostgresDsn(
            f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
        )

class RedisSettings(BaseSettings, ConfigMixin):
    user: str | None = os.getenv("REDIS_USER")
    password: str | None = os.getenv("REDIS_PASSWORD")
    host: str | None = os.getenv("REDIS_HOST")
    port: str | None = os.getenv("REDIS_PORT")
    db: str | None = os.getenv("REDIS_DB")

    @property
    def redis_dsn(self) -> RedisDsn:
        return RedisDsn(
            f"redis://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
        )


class SecuritySettings(BaseSettings, ConfigMixin):
    secret_key: str | None = os.getenv("SECRET_KEY")
    access_token_expire_minutes: str | None = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: str | None = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")
    access_token_type: str = 'access'
    refresh_token_type: str = 'refresh'
    algorithm: str = 'HS256'


class Settings(BaseSettings, ConfigMixin):
    api_v1_prefix: str = "/api/v1"
    redis_settings: RedisSettings = RedisSettings()
    postgres_settings: PostgresSettings = PostgresSettings()
    security_settings: SecuritySettings = SecuritySettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()

SettingsDep = Annotated[Settings, Depends(get_settings)]
