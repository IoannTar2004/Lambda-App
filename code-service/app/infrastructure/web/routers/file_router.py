import os.path

from botocore.exceptions import ClientError
from fastapi import APIRouter, UploadFile
from starlette.responses import StreamingResponse

from infrastructure.config.usecase_config import save_code_usecase, user_files_operations_usecase
from infrastructure.web.dto.save_code_dto import SaveCodeDto

router = APIRouter(prefix="/api/code", tags=["File Controller"])


@router.post("/save-code")
async def upload_code(data: SaveCodeDto):
    """
    upload plain text code
    :param data: includes filename and code
    """
    await save_code_usecase.save(data.filename, data.code)
    return {"ok": True}

@router.post("/upload-file")
async def upload_file(file: UploadFile):
    await user_files_operations_usecase.upload(file)
    return {"ok": True}

@router.get("/download-file")
async def download_file(path: str):
    file = await user_files_operations_usecase.download(path)
    return StreamingResponse(file, media_type="application/octet-stream",
                             headers={
                                 "Content-Disposition": f'attachment; filename="{os.path.basename(path)}"'
                             })

@router.get("/listdir")
async def listdir(path: str):
    files = await user_files_operations_usecase.listdir(path)
    return files