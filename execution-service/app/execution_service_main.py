import asyncio
import os
import sys

from contextlib import asynccontextmanager

import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import infrastructure.messaging.kafka.consumers
from fastapi import FastAPI
from faststream import FastStream

from application.utils.dir_cleaner import dir_cleaner_start
from custom_openapi import custom_openapi
from infrastructure.cache.redis_connection import redis_connection
from infrastructure.config.consul import service_register, service_unregister
from infrastructure.messaging.kafka.kafka import broker
from infrastructure.security.jwt_middleware import JWTMiddleware
from infrastructure.web.routers.log_router import log_router
from settings import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # if sys.platform == "win32":
        # На Windows нужно использовать ProactorEventLoop
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    process = await asyncio.create_subprocess_exec(
        "cmd", "/c", "echo Hello",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()
    print(stdout.decode())

    if not os.path.exists(settings.CODE_ARCHIVES_DIRECTORY):
        os.mkdir(settings.CODE_ARCHIVES_DIRECTORY)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(dir_cleaner_start, 'interval', seconds=3600,
                      args=[settings.CODE_ARCHIVES_DIRECTORY, settings.CODE_ARCHIVES_CLEAN_INTERVAL_SECONDS])
    scheduler.start()

    fast_stream = FastStream(broker)
    await fast_stream.start()
    await service_register()
    await redis_connection.start(settings.REDIS_HOST, settings.REDIS_PORT)

    yield

    scheduler.shutdown()
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
    uvicorn.run("execution_service_main:app", port=8003, reload=True)