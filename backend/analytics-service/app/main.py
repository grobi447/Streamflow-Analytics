from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import analytics

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(title="Analytics Service", lifespan=lifespan)
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])

@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}