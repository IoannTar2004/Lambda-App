import jwt
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from starlette.responses import JSONResponse

from settings import settings


class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        public_paths = ["/health", "/api/code/get-jwt-token", "/docs", "/openapi.json"]

        if request.url.path in public_paths:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JSONResponse(status_code=401, content="Authentication credentials were not provided")

        try:
            token = auth_header.replace("Bearer ", "")
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_SECRET_ALGORITHM])
            request.state.credentials = payload
        except jwt.ExpiredSignatureError:
            return JSONResponse(status_code=401, content="Signature has expired")
        except jwt.InvalidTokenError:
            return JSONResponse(status_code=401, content="Invalid token")

        return await call_next(request)