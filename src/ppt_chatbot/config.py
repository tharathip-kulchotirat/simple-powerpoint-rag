import os
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    TEMP_DIR: Path = Path("./temp")
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    LOG_LEVEL: str = "INFO"
    MAX_FILE_SIZE_MB: int = 50

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"