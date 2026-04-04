from contextlib import asynccontextmanager

import redis.asyncio as redis
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from faststream import FastStream

from custom_openapi import custom_openapi
from infrastructure.config.consul import service_register, service_unregister
from infrastructure.messaging.kafka.kafka import Kafka
from infrastructure.security.jwt_middleware import JWTMiddleware
from infrastructure.storage.async_s3_notification_service import AsyncS3NotificationService
from infrastructure.web.routers.events_router import events_router
from infrastructure.web.routers.execution_logs_router import execution_logs_router
from infrastructure.web.routers.functions_router import functions_router
from infrastructure.web.routers.project_router import project_router
from settings import settings

load_dotenv(settings.Config.env_file)

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.cache = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
    app.state.s3_service = AsyncS3NotificationService(settings.S3_USER_URL,
                                                   settings.S3_USER_ACCESS_KEY, settings.S3_USER_SECRET_KEY)
    await service_register()
    # kafka = Kafka(settings.KAFKA_BOOTSTRAP_SERVERS)
    # fast_stream = FastStream(kafka.broker)
    # await fast_stream.start()
    # app.state.publisher = kafka

    yield

    # await fast_stream.stop()
    await service_unregister()
    await app.state.cache.close()


app = FastAPI(lifespan=lifespan)
app.include_router(functions_router)
app.include_router(events_router)
app.include_router(project_router)
app.include_router(execution_logs_router)

app.add_middleware(JWTMiddleware)

app.openapi = lambda: custom_openapi(app)


@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("events_service_main:app", port=8002, reload=True)