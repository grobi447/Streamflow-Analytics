import httpx
from fastapi import Request, HTTPException
from app.config import settings

async def verify_token(request: Request) -> dict:
    authorization = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.AUTH_SERVICE_URL}/auth/verify",
            headers={"Authorization": authorization}
        )
        data = response.json()
        if not data.get("valid"):
            raise HTTPException(status_code=401, detail="Invalid token")
        return data.get("user")