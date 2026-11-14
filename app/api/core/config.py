import json
from functools import lru_cache
from typing import Annotated, Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Backend Starter"
    APP_ENV: str = "development"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    DATABASE_URL: str

    CORS_ORIGINS: Annotated[list[str], NoDecode] = Field(
        default_factory=lambda: ["http://localhost:3000"]
    )

    TZ: str = "Asia/Jakarta"

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: Any) -> Any:
        if isinstance(value, str):
            value = value.strip()

            if value.startswith("["):
                return json.loads(value)

            return [origin.strip() for origin in value.split(",") if origin.strip()]

        return value

    model_config = SettingsConfigDict(
        case_sensitive=True,
        extra="ignore",
    )

    # Better Auth JWT
    AUTH_JWKS_URL: str
    AUTH_ISSUER: str
    AUTH_AUDIENCE: str
    AUTH_JWT_ALGORITHM: str = "EdDSA"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
