import httpx
from fastapi import APIRouter, Depends
from app.config import settings
from app.middleware.auth_middleware import verify_token

router = APIRouter()

@router.post("/ingest/event")
async def ingest_event(event: dict, user=Depends(verify_token)):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.INGESTION_SERVICE_URL}/ingest/event",
            json=event
        )
        return response.json()