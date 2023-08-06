from pydantic import BaseSettings
from functools import lru_cache

@lru_cache()
def get_settings():
    return Settings()


class Settings(BaseSettings):
  # project config 
  PROJECT_NAME: str = "Store Monitoring API"
  PROJECT_VERSION: str = "0.0.1"
  PROJECT_DESCRIPTION: str = "Store Monitoring API"
  PROJECT_DOCS_URL: str = "/api/docs"

  # database config
  DB_USER: str = "postgres"
  DB_PASSWORD: str = "postgres"
  DB_HOST: str = "localhost"
  DB_PORT: str = "5432"
  DB_NAME: str = "store_monitor"
  DB_POOL_SIZE: int = 20
  DB_MAX_OVERFLOW: int = 20
  DB_POOL_RECYCLE: int = 3600

  # celery config 
  CELERY_BROKER_URL: str = "redis://:redis@redis:6379/0"


  # taking env file
  class Config:
    env_file = ".env"
    case_sensitive = True





