import os.path

from fastapi import APIRouter, UploadFile
from starlette.responses import StreamingResponse

from infrastructure.config.usecase_config import save_code_usecase, storage_operations_usecase
from infrastructure.web.model.save_code_model import CodeRequest

router = APIRouter(prefix="/api/code", tags=["File Controller"])


@router.post("/save-code")
async def upload_code(data: CodeRequest):
    """
    upload plain text code
    :param data: includes filename and code
    """
    await save_code_usecase.save(data.filename, data.code)
    return {"ok": True}


@router.post("/upload-user-file")
async def upload_file(file: UploadFile):
    await storage_operations_usecase.upload(file)
    return {"ok": True}


@router.get("/download-user-file")
async def download_file(filename: str):
    file = await storage_operations_usecase.download(filename)
    return StreamingResponse(file, media_type="application/octet-stream",
                             headers={
                                 "Content-Disposition": f'attachment; filename="{os.path.basename(filename)}"'
                             })
