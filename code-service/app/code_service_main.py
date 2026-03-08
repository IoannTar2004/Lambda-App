from contextlib import asynccontextmanager

import redis.asyncio as redis
import uvicorn
from dotenv import load_dotenv

from fastapi import FastAPI

from infrastructure.config.consul import service_register, service_unregister
from infrastructure.storage.async_s3_service import AsyncS3Service
from infrastructure.web.routers.file_router import router

from settings import settings

load_dotenv(settings.Config.env_file)

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.cache = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
    app.state.storage = AsyncS3Service(settings.S3_URL, settings.S3_ACCESS_KEY,settings.S3_SECRET_KEY)
    await service_register()
    yield
    await service_unregister()
    await app.state.cache.close()

app = FastAPI(lifespan=lifespan)
app.include_router(router)

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("code_service_main:app", port=8001, reload=True)