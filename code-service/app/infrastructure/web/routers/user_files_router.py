import os.path
from typing import cast

from fastapi import APIRouter, UploadFile, Request
from mypy_boto3_s3 import S3Client
from starlette.responses import StreamingResponse

from application.usecase.save_code_usecase import SaveCodeUseCase
from application.usecase.user_files_operations_usecase import UserFilesOperationsUseCase
from infrastructure.web.dto.user_files.save_code_dto import SaveCodeDto

file_router = APIRouter(prefix="/api/code", tags=["User files"])


@file_router.post("/save-code")
async def save_code(data: SaveCodeDto, request: Request):
    """
    upload plain text code
    :param data: includes filename and code
    :param request: request object
    """
    save_code_usecase = SaveCodeUseCase(request.app.state.storage, request.app.state.cache)
    await save_code_usecase.save(data.path, data.code)
    return {"success": True}

@file_router.post("/upload-file")
async def upload_file(file: UploadFile, directory: str, request: Request):
    user_files_operations_usecase = UserFilesOperationsUseCase(request.app.state.storage, request.app.state.cache)
    await user_files_operations_usecase.upload(file, directory)
    return {"success": True}

@file_router.get("/download-file")
async def download_file(path: str, request: Request):
    user_files_operations_usecase = UserFilesOperationsUseCase(request.app.state.storage)
    file = await user_files_operations_usecase.download(path)
    return StreamingResponse(file, media_type="application/octet-stream",
                             headers={
                                 "Content-Disposition": f'attachment; filename="{os.path.basename(path)}"'
                             })

@file_router.get("/listdir")
async def listdir(path: str, request: Request):
    user_files_operations_usecase = UserFilesOperationsUseCase(request.app.state.storage)
    files = await user_files_operations_usecase.listdir(path)
    return files

@file_router.delete("/delete-file")
async def delete_file(path: str, request: Request):
    user_files_operations_usecase = UserFilesOperationsUseCase(request.app.state.storage)
    await user_files_operations_usecase.delete(path)
    return {"success": True}
