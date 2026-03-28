import httpx
from fastapi import APIRouter, Depends
from app.config import settings
from app.middleware.auth_middleware import verify_token

router = APIRouter()

@router.get("/alerts/active")
async def get_active_alerts(user=Depends(verify_token)):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.ALERT_SERVICE_URL}/alerts/active")
        return response.json()

@router.get("/alerts/all")
async def get_all_alerts(limit: int = 100, user=Depends(verify_token)):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.ALERT_SERVICE_URL}/alerts/all?limit={limit}")
        return response.json()

@router.put("/alerts/resolve/{alert_id}")
async def resolve_alert(alert_id: str, user=Depends(verify_token)):
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{settings.ALERT_SERVICE_URL}/alerts/resolve/{alert_id}")
        return response.json()

@router.post("/alerts/check")
async def check_event(event: dict, user=Depends(verify_token)):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.ALERT_SERVICE_URL}/alerts/check",
            json=event
        )
        return response.json()