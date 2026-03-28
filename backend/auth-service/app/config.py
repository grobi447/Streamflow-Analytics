from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    VERTICA_HOST: str
    VERTICA_PORT: int
    VERTICA_USER: str
    VERTICA_PASSWORD: str
    VERTICA_DATABASE: str
    JWT_SECRET: str
    JWT_EXPIRY: int = 3600

    class Config:
        env_file = "../.env"

settings = Settings()