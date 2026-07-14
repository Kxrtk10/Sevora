from functools import cached_property

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "ClinicFlow API"
    app_env: str = "development"
    app_debug: bool = True
    api_v1_prefix: str = "/api/v1"
    backend_cors_origins_raw: str = Field(
        default="http://localhost:5173",
        alias="BACKEND_CORS_ORIGINS",
    )
    database_url: str = "postgresql+asyncpg://clinicflow:clinicflow@localhost:5432/clinicflow"
    log_level: str = "INFO"

    @cached_property
    def backend_cors_origins(self) -> list[str]:
        return [
            origin.strip() for origin in self.backend_cors_origins_raw.split(",") if origin.strip()
        ]

    @property
    def is_development(self) -> bool:
        return self.app_env.lower() == "development"


settings = Settings()
