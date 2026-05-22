from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    OPENAPI_URL: str
    OPENAI_API_KEY: str
    FILE_ALLOW_EXTS: list[str]
    MAX_FILE_SIZE_MB: int
    FILE_DEFAULT_CHUNK_SIZE: int

    MONGODB_URI: str = "mongodb://admin:password123@localhost:27017"
    MONGODB_DB_NAME: str = "rag_db"


    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


@lru_cache
def get_settings():
    return Settings()

