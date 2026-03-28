from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from app.config import settings
from app.models.user import User, UserLogin, UserRegister, TokenResponse, VerifyResponse, UserRole
from app.database.repositories.user_repository import UserRepository

class AuthService:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    def register(self, user: UserRegister) -> User:
        return self._repository.create(user)

    def login(self, credentials: UserLogin) -> TokenResponse:
        user_data = self._repository.get_by_username(credentials.username)
        if not user_data:
            raise ValueError("Invalid username or password")

        if not self._repository.verify_password(credentials.password, user_data['password']):
            raise ValueError("Invalid username or password")

        user = User(
            user_id=user_data['user_id'],
            username=user_data['username'],
            email=user_data['email'],
            role=UserRole(user_data['role']),
            created_at=user_data['created_at']
        )

        token = self._create_token(user)

        return TokenResponse(
            access_token=token,
            expires_in=settings.JWT_EXPIRY,
            user=user
        )

    def verify(self, token: str) -> VerifyResponse:
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=["HS256"]
            )
            user_data = self._repository.get_by_username(payload['username'])
            if not user_data:
                return VerifyResponse(valid=False)

            user = User(
                user_id=user_data['user_id'],
                username=user_data['username'],
                email=user_data['email'],
                role=UserRole(user_data['role']),
                created_at=user_data['created_at']
            )
            return VerifyResponse(valid=True, user=user)
        except JWTError:
            return VerifyResponse(valid=False)

    def _create_token(self, user: User) -> str:
        expire = datetime.now() + timedelta(seconds=settings.JWT_EXPIRY)
        payload = {
            'user_id': user.user_id,
            'username': user.username,
            'role': user.role.value,
            'exp': expire
        }
        return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

auth_service = AuthService(repository=UserRepository())