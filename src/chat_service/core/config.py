from functools import lru_cache
from typing import Annotated, Self

from dotenv import load_dotenv
from fastapi import Depends
from pydantic import Field, PostgresDsn, RedisDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class ConfigMixin:
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    @classmethod
    def from_env(cls) -> Self:
        return cls()


class PostgresSettings(BaseSettings, ConfigMixin):
    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: SecretStr

    @property
    def postgres_dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.postgres_user,
            password=self.postgres_password.get_secret_value(),
            host=self.postgres_host,
            port=self.postgres_port,
            path=self.postgres_db,
        )


class RedisSettings(BaseSettings, ConfigMixin):
    redis_user: str
    redis_password: str
    redis_host: str
    redis_port: int
    redis_db: str

    @property
    def redis_dsn(self) -> RedisDsn:
        return RedisDsn.build(
            scheme="redis",
            username=self.redis_user,
            password=self.redis_password,
            host=self.redis_host,
            port=self.redis_port,
            path=self.redis_db,
        )


class SecuritySettings(BaseSettings, ConfigMixin):
    secret_key: SecretStr
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    access_token_type: str = "access"
    refresh_token_type: str = "refresh"
    algorithm: str = "HS256"


class Settings(BaseSettings, ConfigMixin):
    api_v1_prefix: str = "/api/v1"
    redis_settings: RedisSettings = Field(default_factory=RedisSettings.from_env)
    postgres_settings: PostgresSettings = Field(default_factory=PostgresSettings.from_env)
    security_settings: SecuritySettings = Field(default_factory=SecuritySettings.from_env)


@lru_cache
def get_settings() -> Settings:
    return Settings()


SettingsDep = Annotated[Settings, Depends(get_settings)]
