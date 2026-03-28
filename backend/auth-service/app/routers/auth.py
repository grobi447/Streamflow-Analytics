from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from app.models.user import UserLogin, UserRegister, User, TokenResponse, VerifyResponse
from app.services.auth_service import auth_service

router = APIRouter()

@router.post("/register", response_model=User)
async def register(user: UserRegister) -> User:
    try:
        return auth_service.register(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin) -> TokenResponse:
    try:
        return auth_service.login(credentials)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/verify", response_model=VerifyResponse)
async def verify(authorization: Optional[str] = Header(None)) -> VerifyResponse:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = authorization.split(" ")[1]
    return auth_service.verify(token)