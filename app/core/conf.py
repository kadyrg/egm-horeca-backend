from pydantic_settings import BaseSettings
from pathlib import Path
from typing import List


BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    db_user: str
    db_pass: str
    db_name: str
    db_port: str
    db_host: str

    email_confirm_token_secret: str

    email_host: str
    email_port: int
    email_user: str
    email_pass: str

    email_token_validity: int = 3600 # seconds

    access_token_secret: str
    refresh_token_secret: str

    supported_languages: List[str] = {"en", "ro"}

    jwt_algorithm: str = "HS256"

    access_token_validity: int = 15 # minutes
    refresh_token_validity: int = 30 # days

    base_url: Path = BASE_DIR
    media_url: Path = BASE_DIR / "media"

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"

settings = Settings()
