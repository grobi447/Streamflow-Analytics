from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import auth, ingestion, analytics, alerts

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(title="API Gateway")

app.include_router(auth.router, tags=["auth"])
app.include_router(ingestion.router, tags=["ingestion"])
app.include_router(analytics.router, tags=["analytics"])
app.include_router(alerts.router, tags=["alerts"])

@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}