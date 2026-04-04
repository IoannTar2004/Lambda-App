from datetime import timezone, timedelta, datetime

import jwt
from fastapi import APIRouter

from settings import settings

auth_router = APIRouter(prefix="/api/code/auth", tags=["Auth"])

@auth_router.get("/get-jwt-token")
async def get_jwt_token(user_id: int):
    """Простая реализация получения jwt-токена. Имитация авторизованного пользователя VK Cloud"""
    expire = datetime.now(timezone.utc) + timedelta(seconds=settings.JWT_SECRET_EXPIRES_SECONDS)
    payload = {
        "user_id": user_id,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "role": "user",
    }
    return {
        "access_token": jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_SECRET_ALGORITHM),
    }

