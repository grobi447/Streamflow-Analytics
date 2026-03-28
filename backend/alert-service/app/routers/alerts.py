from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from typing import List
from app.models.alert import Alert, AlertListResponse, AlertResponse
from app.services.alert_service import alert_service, manager

router = APIRouter()

@router.get("/active", response_model=List[Alert])
async def get_active_alerts() -> List[Alert]:
    try:
        return alert_service.get_active_alerts()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/all", response_model=List[Alert])
async def get_all_alerts(limit: int = 100) -> List[Alert]:
    try:
        return alert_service.get_all_alerts(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/resolve/{alert_id}", response_model=AlertResponse)
async def resolve_alert(alert_id: str) -> AlertResponse:
    try:
        alert_service.resolve_alert(alert_id)
        return AlertResponse(status="success", message=f"Alert {alert_id} resolved")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/check", response_model=AlertResponse)
async def check_event(event: dict) -> AlertResponse:
    try:
        await alert_service.check_and_create_alert(event)
        return AlertResponse(status="success", message="Event checked for alerts")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)