from contextlib import asynccontextmanager

import uvicorn
import infrastructure.messaging.kafka.consumers
from fastapi import FastAPI
from faststream import FastStream

from infrastructure.messaging.kafka.kafka import broker


@asynccontextmanager
async def lifespan(app: FastAPI):
    fast_stream = FastStream(broker)
    await fast_stream.start()
    yield
    await fast_stream.stop()


app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    uvicorn.run("execution_service_main:app", port=8003, reload=True)