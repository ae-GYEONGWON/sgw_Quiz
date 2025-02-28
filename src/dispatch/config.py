from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import logging

from functools import lru_cache

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


# ✅ 캐싱된 설정 객체 생성
@lru_cache()
def get_settings() -> Settings:
    return Settings()

# ✅ 캐시 초기화 함수 (환경 변수 변경 후 호출)
def reload_settings():
    get_settings.cache_clear()  # ✅ 캐시 초기화
    log.info("🔄 Settings reloaded!")  # 로그 출력
