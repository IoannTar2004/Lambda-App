import os
from contextlib import asynccontextmanager

import redis.asyncio as redis
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from infrastructure.config.consul import service_register, service_unregister
from infrastructure.web.routers.events_router import router
from settings import settings

load_dotenv(settings.Config.env_file)

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = redis.Redis(host='localhost', port=6379, db=0)
    await service_register()
    yield
    await service_unregister()
    await app.state.redis.close()


app = FastAPI(lifespan=lifespan)
app.include_router(router)


@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("events_service_main:app", port=8002, reload=True)