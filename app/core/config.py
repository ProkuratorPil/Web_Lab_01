from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    PORT: int = 4200

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()