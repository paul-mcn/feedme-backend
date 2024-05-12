from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    AWS_BUCKET_NAME: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION_NAME: str
    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_environment_settings():
    return EnvironmentSettings()
