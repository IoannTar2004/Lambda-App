import uvicorn
from fastapi import FastAPI
from infrastructure.web.controllers.file_controller import router

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("upload_code_service_main:app", reload=True)