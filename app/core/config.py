from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DB_USER: str = "DB_USER"
    DB_PASSWORD: str = "DB_PASSWORD"
    DB_HOST: str = "DB_HOST"
    DB_PORT: str = "DB_PORT"
    DB_NAME: str = "DB_NAME"

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }


settings = Settings()
