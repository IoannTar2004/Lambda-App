from contextlib import asynccontextmanager

import uvicorn
import infrastructure.messaging.kafka.consumers

from fastapi import FastAPI
from faststream import FastStream

from custom_openapi import custom_openapi
from infrastructure.cache.redis_connection import redis_connection
from infrastructure.config.consul import service_register, service_unregister
from infrastructure.docker.mounts import DocketMounts
from infrastructure.messaging.kafka.kafka import broker
from infrastructure.security.jwt_middleware import JWTMiddleware
from infrastructure.web.routers.log_router import log_router
from settings import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    DocketMounts.set_mounts()
    fast_stream = FastStream(broker)
    await fast_stream.start()
    await service_register()
    await redis_connection.start(settings.REDIS_HOST, settings.REDIS_PORT)

    yield

    await service_unregister()
    await fast_stream.stop()
    await redis_connection.close()


app = FastAPI(lifespan=lifespan)
app.include_router(log_router)
app.add_middleware(JWTMiddleware)

app.openapi = lambda: custom_openapi(app)

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("execution_service_main:app", host="0.0.0.0", port=8003,  reload=True)
