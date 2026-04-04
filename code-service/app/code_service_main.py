import datetime
from contextlib import asynccontextmanager
from datetime import timezone, timedelta

import jwt
import uvicorn
from dotenv import load_dotenv

from fastapi import FastAPI

from custom_openapi import custom_openapi
from infrastructure.config.consul import service_register, service_unregister
from infrastructure.security.jwt_middleware import JWTMiddleware
from infrastructure.storage.async_s3_service import S3Service
from infrastructure.web.routers.auth_router import auth_router
from infrastructure.web.routers.files_router import files_router
from infrastructure.web.routers.user_files_router import user_files_router
from infrastructure.web.routers.zip_router import zip_router

from settings import settings

load_dotenv(settings.Config.env_file)

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.s3_code = S3Service(settings.S3_CODE_URL, settings.S3_CODE_ACCESS_KEY, settings.S3_CODE_SECRET_KEY)
    await service_register()
    yield
    await service_unregister()

app = FastAPI(lifespan=lifespan)
app.include_router(files_router)
app.include_router(user_files_router)
app.include_router(zip_router)
app.include_router(auth_router)

app.add_middleware(JWTMiddleware)

app.openapi = lambda: custom_openapi(app)

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("code_service_main:app", port=8001, reload=True)