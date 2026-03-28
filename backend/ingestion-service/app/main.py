from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import ingest
from app.database.repositories.event_repository import EventRepository

@asynccontextmanager
async def lifespan(app: FastAPI):
    EventRepository().init_table()
    yield

app = FastAPI(title="Ingestion Service", lifespan=lifespan)
app.include_router(ingest.router, prefix="/ingest", tags=["ingest"])

@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}