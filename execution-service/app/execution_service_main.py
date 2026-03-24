import asyncio
import os
from contextlib import asynccontextmanager

import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import infrastructure.messaging.kafka.consumers
from fastapi import FastAPI
from faststream import FastStream

from application.utils.dir_cleaner import dir_cleaner_start
from infrastructure.config.consul import service_register, service_unregister
from infrastructure.messaging.kafka.kafka import broker
from settings import settings

async def hello():
    print("hello")

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.path.exists(settings.CODE_ARCHIVES_DIRECTORY):
        os.mkdir(settings.CODE_ARCHIVES_DIRECTORY)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(dir_cleaner_start, 'interval', seconds=5,
                      args=[settings.CODE_ARCHIVES_DIRECTORY, settings.CODE_ARCHIVES_CLEAN_INTERVAL_SECONDS])
    scheduler.start()

    fast_stream = FastStream(broker)
    await fast_stream.start()
    await service_register()

    yield

    scheduler.shutdown()
    await service_unregister()
    await fast_stream.stop()


app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("execution_service_main:app", port=8003, reload=True)