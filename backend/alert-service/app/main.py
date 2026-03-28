from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import alerts
from app.database.repositories.alert_repository import AlertRepository

@asynccontextmanager
async def lifespan(app: FastAPI):
    AlertRepository().init_table()
    yield

app = FastAPI(title="Alert Service", lifespan=lifespan)
app.include_router(alerts.router, prefix="/alerts", tags=["alerts"])

@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}