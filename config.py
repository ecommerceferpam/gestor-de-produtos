# backend/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # credenciais sensíveis
    MAGENTO_API_KEY: str
    MELI_API_KEY: Optional[str] = None
    ERP_API_KEY: Optional[str] = None
    GEMINI_API_KEY: str
    AUTCOM_WS_AUTH: str
    AUTCOM_GETPRODUCT_PATH: str
    AUTCOM_PATCHPRODUCT_PATH: str
    MERCOS_COMPANY_TOKEN: Optional[str] = None
    TINY_API_KEY: str

    # configurações gerais
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    class Config:
        env_file = ".env"          # usado em dev local
        env_file_encoding = "utf-8"

settings = Settings()
