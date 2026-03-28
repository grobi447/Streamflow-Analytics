from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    VIEWER = "VIEWER"

class UserLogin(BaseModel):
    username: str
    password: str

class UserRegister(BaseModel):
    username: str
    password: str
    email: str
    role: UserRole = UserRole.VIEWER

class User(BaseModel):
    user_id: str
    username: str
    email: str
    role: UserRole
    created_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: User

class VerifyResponse(BaseModel):
    valid: bool
    user: User | None = None