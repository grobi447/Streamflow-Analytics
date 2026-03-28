from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    VERTICA_HOST: str
    VERTICA_PORT: int
    VERTICA_USER: str
    VERTICA_PASSWORD: str
    VERTICA_DATABASE: str
    LATENCY_THRESHOLD: float = 100.0
    PACKET_LOSS_THRESHOLD: float = 5.0
    SIGNAL_THRESHOLD: float = -90.0

    class Config:
        env_file = "../.env"

settings = Settings()