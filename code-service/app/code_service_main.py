from contextlib import asynccontextmanager

import redis.asyncio as redis
import uvicorn
from dotenv import load_dotenv

from fastapi import FastAPI, Request

from infrastructure.config.consul import service_register, service_unregister
from infrastructure.storage.async_s3_service import S3Service
from infrastructure.web.routers.files_router import files_router
from infrastructure.web.routers.user_files_router import user_files_router
from infrastructure.web.routers.zip_router import zip_router

from settings import settings

load_dotenv(settings.Config.env_file)

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.cache = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
    app.state.s3_code = S3Service(settings.S3_CODE_URL, settings.S3_CODE_ACCESS_KEY, settings.S3_CODE_SECRET_KEY)
    await service_register()
    yield
    await service_unregister()
    await app.state.cache.close()

app = FastAPI(lifespan=lifespan)
app.include_router(files_router)
app.include_router(user_files_router)
app.include_router(zip_router)

@app.get("/health")
async def health(request: Request):
    print(await request.app.state.s3_code.recursive_listdir("user-code", ""))
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("code_service_main:app", port=8001, reload=True)