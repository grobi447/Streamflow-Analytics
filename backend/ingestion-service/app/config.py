from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    VERTICA_HOST: str
    VERTICA_PORT: int
    VERTICA_USER: str
    VERTICA_PASSWORD: str
    VERTICA_DATABASE: str
    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_TOPIC: str

    class Config:
        env_file = "../.env"

settings = Settings()