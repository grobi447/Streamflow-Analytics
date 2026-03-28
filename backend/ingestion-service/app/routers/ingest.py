from fastapi import APIRouter, HTTPException
from app.models.network_event import NetworkEvent
from app.models.responses import IngestResponse, ErrorResponse
from app.services.ingest_service import ingest_service

router = APIRouter()

@router.post(
    "/event",
    response_model=IngestResponse,
    responses={500: {"model": ErrorResponse}}
)
async def ingest_event(event: NetworkEvent) -> IngestResponse:
    try:
        return ingest_service.process(event)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                status="error",
                message="Failed to process event",
                detail=str(e)
            ).model_dump()
        )