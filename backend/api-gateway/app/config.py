from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AUTH_SERVICE_URL: str = "http://auth-service:8001"
    INGESTION_SERVICE_URL: str = "http://ingestion-service:8002"
    ANALYTICS_SERVICE_URL: str = "http://analytics-service:8003"
    ALERT_SERVICE_URL: str = "http://alert-service:8004"

    class Config:
        env_file = "../.env"

settings = Settings()