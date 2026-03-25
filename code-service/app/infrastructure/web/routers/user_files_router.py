import os.path

from fastapi import APIRouter, UploadFile, Request
from fastapi.params import Form
from starlette.responses import StreamingResponse

from application.usecase.save_code_usecase import SaveCodeUseCase
from application.usecase.files_operations_usecase import FilesOperationsUseCase
from infrastructure.web.dto.user_files.save_code_dto import SaveCodeDto
from settings import settings

user_files_router = APIRouter(prefix="/api/user-files", tags=["User files"])


@user_files_router.post("/save-code")
async def save_code(data: SaveCodeDto, request: Request):
    """
    upload plain text code
    :param data: includes filename and code
    :param request: request object
    """
    save_code_usecase = SaveCodeUseCase(request.app.state.s3_code, request.app.state.cache)
    await save_code_usecase.save(data.path, data.code)
    return {"success": True}

@user_files_router.post("/upload-file")
async def upload_file(request: Request, file: UploadFile, directory: str = Form(max_length=256)):
    files_operations_usecase = FilesOperationsUseCase(request.app.state.s3_code, request.app.state.cache)
    await files_operations_usecase.upload(settings.S3_USER_CODE_BUCKET, file, directory)
    return {"success": True}

@user_files_router.get("/download-file")
async def download_file(path: str, request: Request):
    files_operations_usecase = FilesOperationsUseCase(request.app.state.s3_code)
    file = await files_operations_usecase.download(settings.S3_USER_CODE_BUCKET, path)
    return StreamingResponse(file, media_type="application/octet-stream",
                             headers={
                                 "Content-Disposition": f'attachment; filename="{os.path.basename(path)}"'
                             })

@user_files_router.get("/listdir")
async def listdir(path: str, request: Request):
    files_operations_usecase = FilesOperationsUseCase(request.app.state.s3_code)
    files = await files_operations_usecase.listdir(settings.S3_USER_CODE_BUCKET, path)
    return files

@user_files_router.delete("/delete-file")
async def delete_file(path: str, request: Request):
    files_operations_usecase = FilesOperationsUseCase(request.app.state.s3_code)
    await files_operations_usecase.delete(settings.S3_USER_CODE_BUCKET, path)
    return {"success": True}
