from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv

from fastapi import FastAPI

from infrastructure.config.consul import service_register, service_unregister
from infrastructure.web.routers.file_router import router

from settings import settings

load_dotenv(settings.Config.env_file)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await service_register()
    yield
    await service_unregister()

app = FastAPI(lifespan=lifespan)
app.include_router(router)

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("code_service_main:app", port=8001, reload=True)