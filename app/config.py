from functools import lru_cache
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "Rabe Leads")
    app_env: str = os.getenv("APP_ENV", "development")
    secret_key: str = os.getenv("SECRET_KEY", "change-me")

    mysql_host: str = os.getenv("MYSQL_HOST", "127.0.0.1")
    mysql_port: int = int(os.getenv("MYSQL_PORT", "3306"))
    mysql_database: str = os.getenv("MYSQL_DATABASE", "rabe_leads")
    mysql_user: str = os.getenv("MYSQL_USER", "root")
    mysql_password: str = os.getenv("MYSQL_PASSWORD", "")

    google_places_api_key: str = os.getenv("GOOGLE_PLACES_API_KEY", "")
    google_pagespeed_api_key: str = os.getenv("GOOGLE_PAGESPEED_API_KEY", "")

    smtp_host: str = os.getenv("SMTP_HOST", "")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_user: str = os.getenv("SMTP_USER", "")
    smtp_password: str = os.getenv("SMTP_PASSWORD", "")
    smtp_from_email: str = os.getenv("SMTP_FROM_EMAIL", "")
    smtp_from_name: str = os.getenv("SMTP_FROM_NAME", "Rabe Soluções Digitais")
    smtp_use_tls: bool = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
    smtp_use_ssl: bool = os.getenv("SMTP_USE_SSL", "false").lower() == "true"

    request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", "20"))
    user_agent: str = os.getenv("USER_AGENT", "RabeLeads/1.0")

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
            "?charset=utf8mb4"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
