import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from infrastructure.web.controllers.file_controller import router
from settings import settings

app = FastAPI()
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
)

if __name__ == "__main__":
    uvicorn.run("upload_code_service_main:app", reload=True)