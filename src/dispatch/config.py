from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import logging

# from functools import lru_cache

log = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):

    # MySQL 설정 정보
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_ROOT_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    LOG_LEVEL: int = logging.WARNING

    model_config = SettingsConfigDict(env_file=str(BASE_DIR / ".env"), extra="ignore")


def get_setting():
    return Settings()
