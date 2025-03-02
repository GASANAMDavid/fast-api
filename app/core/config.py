import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

dotenv_file = ".env.test" if os.getenv("ENV", 'test') else ".env"
load_dotenv(dotenv_path=dotenv_file, override=True)

class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    PG_ADMIN_URL: str = os.getenv("PG_ADMIN_URL")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./db/dev_db.sqlite")
    ROLE_NAME: str = os.getenv("ROLE_NAME", "user")
    DB_NAME: str = os.getenv("DB_NAME", "test_db")


settings = Settings()
