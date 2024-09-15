from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, Field

class Settings(BaseSettings):
    # Application settings
    service_name: str = "Payment Service"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    debug: bool = False
    log_level: str = "info"

    # Database settings
    db_dsn: PostgresDsn = Field(..., alias="DATABASE_URL")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }
