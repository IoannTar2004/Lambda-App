from fastapi import APIRouter, UploadFile
from infrastructure.config.usecase_config import upload_code_usecase

router = APIRouter(prefix="/users", tags=["File Controller"])


@router.post("/upload-code")
async def upload_code(uploaded: UploadFile):
    await upload_code_usecase.upload_code(uploaded)
    return {"ok": True}
