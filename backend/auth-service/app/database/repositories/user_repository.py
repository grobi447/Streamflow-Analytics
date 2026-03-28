import uuid
from datetime import datetime
from typing import Optional
from passlib.context import CryptContext
from app.database.connection import vertica_connection
from app.models.user import User, UserRegister, UserRole

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:
    def init_table(self) -> None:
        with vertica_connection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id     VARCHAR(36),
                    username    VARCHAR(100),
                    email       VARCHAR(200),
                    password    VARCHAR(200),
                    role        VARCHAR(20),
                    created_at  TIMESTAMP
                )
            """)
            conn.commit()

    def create(self, user: UserRegister) -> User:
        user_id = str(uuid.uuid4())
        hashed_password = pwd_context.hash(user.password)
        created_at = datetime.utcnow()

        with vertica_connection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (
                    user_id, username, email, password, role, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                user_id,
                user.username,
                user.email,
                hashed_password,
                user.role.value,
                created_at
            ))
            conn.commit()

        return User(
            user_id=user_id,
            username=user.username,
            email=user.email,
            role=user.role,
            created_at=created_at
        )

    def get_by_username(self, username: str) -> Optional[dict]:
        with vertica_connection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT user_id, username, email, password, role, created_at
                FROM users
                WHERE username = %s
            """, (username,))
            row = cursor.fetchone()
            if row is None:
                return None
            return {
                'user_id': row[0],
                'username': row[1],
                'email': row[2],
                'password': row[3],
                'role': row[4],
                'created_at': row[5]
            }

    def verify_password(self, plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)