from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
import asyncio

from infrastructure.messaging.kafka_config import kafka
from infrastructure.web.controllers.events_controller import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await kafka.producer_start(app)
    yield
    await kafka.producer_stop()

app = FastAPI(lifespan=lifespan)
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("events_service_main:app", port=8002, reload=True)