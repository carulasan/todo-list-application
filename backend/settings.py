import os
from typing import Optional
from pydantic import BaseModel


class SystemSettings(BaseModel):
    """Initial System Settings loaded from ENV."""

    ENV: str = None
    DEBUG_MODE: Optional[str] = "false"
    ALLOWED_HOST: str = "*"
    CONFIG_NAME: str = "Geoplan-API"


    class Config:
        """Configuration source settings."""

        env_file = None
        env_file_encoding = "utf-8"


class DatabaseClientSettings(BaseModel):
    """Database related settings whether from PostgreSql, Redis, etc.."""

    REDIS_HOST: Optional[str] = None
    REDIS_PORT: Optional[str] = '6379'
    REDIS_DB: Optional[str] = '0'
    DATABASE_ENGINE_POOL_SIZE: Optional[int] = 10
    DATABASE_ENGINE_MAX_OVERFLOW: Optional[int] = 10
    DATABASE_ENGINE_POOL_PING: Optional[int] = 0
    READ_DATABASE_URL: Optional[str] = None
    WRITE_DATABASE_URL: Optional[str] = None
    ENABLE_DB_LOGGING: Optional[str] = "false"

    @property
    def REDIS_URI(self) -> Optional[str]:
        """
        Build the REDIS_URI from the Redis settings.
        Format: redis://<REDIS_HOST>:<REDIS_PORT>/<REDIS_DB>
        """
        if not self.REDIS_HOST or not self.REDIS_PORT or not self.REDIS_DB:
            return None

        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    
    class Config:
        """Configuration source settings."""

        env_file = None
        env_file_encoding = "utf-8"

# Access os.environ as a dictionary
env_dict = dict(os.environ)

system_settings = SystemSettings.model_validate(env_dict)
db_settings = DatabaseClientSettings.model_validate(env_dict)