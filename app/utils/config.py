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

  # redis config 
  REDIS_HOST: str = "localhost"
  REDIS_PORT: str = "6379"
  REDIS_DB: int = 0
  REDIS_PASSWORD: str = "redis"

  # taking env file
  class Config:
    env_file = ".env"
    case_sensitive = True





