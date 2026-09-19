import os
from functools import lru_cache

from pydantic import RedisDsn, PostgresDsn
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class PostgresSettings(BaseSettings):
    host: str = os.getenv('POSTGRES_HOST')
    port: int = os.getenv('POSTGRES_PORT')
    db: int = os.getenv('POSTGRES_DB')
    user: str = os.getenv('POSTGRES_USER')
    password: str = os.getenv('POSTGRES_PASSWORD')

    @property
    def postgres_dsn(self) -> PostgresDsn:
        return PostgresDsn(
            f'postgresql+asyncg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}'
        )
    class Config:
        env_file = '.env'
        case_sensitive = True


class RedisSettings(BaseSettings):
    user: str = os.getenv('REDIS_USER')
    password: str = os.getenv('REDIS_PASSWORD')
    host: str = os.getenv('REDIS_HOST')
    port: int = os.getenv('REDIS_PORT')
    db: int = os.getenv('REDIS_DB')

    @property
    def redis_dsn(self) -> RedisDsn:
        return RedisDsn(f'redis://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}')

    class Config:
        env_file = '.env'
        case_sensitive = True

class Settings(BaseSettings):
    redis_settings: RedisSettings = RedisSettings()
    postgres_settings: PostgresSettings = PostgresSettings()

    class Config:
        env_file = '.env'
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    return Settings()