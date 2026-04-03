import os.path
from typing import Annotated

from fastapi import APIRouter, UploadFile, Request
from fastapi.params import Form
from pydantic import Field
from starlette.responses import StreamingResponse

from application.usecase.files_operations_usecase import FilesOperationsUseCase
from application.usecase.runnable_list_usecase import RunnableListUseCase
from application.usecase.delete_with_unzip_usecase import DeleteWithUnzip
from infrastructure.web.dto.user_files.delete_files_dto import DeleteFilesDto
from settings import settings

user_files_router = APIRouter(prefix="/api/code/user-files", tags=["User files"])


@user_files_router.post("/upload-file")
async def upload_file(request: Request, file: UploadFile, project_id: int = Form(),
                      directory: str = Form(max_length=256, default="")):
    user_id = request.state.credentials["user_id"]
    files_operations_usecase = FilesOperationsUseCase(request.app.state.s3_code)
    await files_operations_usecase.upload(settings.S3_USER_CODE_BUCKET, file,
                                          f"{user_id}/{project_id}/{directory}")

    return {"success": True}

@user_files_router.get("/download-file")
async def download_file(path: str, project_id: int, request: Request):
    user_id = request.state.credentials["user_id"]
    files_operations_usecase = FilesOperationsUseCase(request.app.state.s3_code)
    file = await files_operations_usecase.download(settings.S3_USER_CODE_BUCKET, f"{user_id}/{project_id}/{path}")
    return StreamingResponse(file, media_type="application/octet-stream",
                             headers={
                                 "Content-Disposition": f'attachment; filename="{os.path.basename(path)}"'
                             })

@user_files_router.get("/listdir")
async def listdir(request: Request, project_id: int, path: str = ""):
    user_id = request.state.credentials["user_id"]
    files_operations_usecase = FilesOperationsUseCase(request.app.state.s3_code)
    files = await files_operations_usecase.listdir(settings.S3_USER_CODE_BUCKET, f"{user_id}/{project_id}/{path}")
    return files

@user_files_router.get("/listdir-all")
async def listdir_all(request: Request, project_id: int, path: str = ""):
    user_id = request.state.credentials["user_id"]
    files_operations_usecase = FilesOperationsUseCase(request.app.state.s3_code)
    files = await files_operations_usecase.listdir_all(settings.S3_USER_CODE_BUCKET, f"{user_id}/{project_id}/{path}")
    return files

@user_files_router.delete("/delete")
async def delete(data: DeleteFilesDto, request: Request):
    user_id = request.state.credentials["user_id"]
    data.keys = [f"{user_id}/{data.project_id}/{k}" for k in data.keys]
    files_operations_usecase = FilesOperationsUseCase(request.app.state.s3_code)
    await files_operations_usecase.delete(settings.S3_USER_CODE_BUCKET, data.keys)
    return {"success": True}

@user_files_router.get("/download-log")
async def download_log(function_id: int, log_id: str, request: Request):
    user_id = request.state.credentials["user_id"]
    files_operations_usecase = FilesOperationsUseCase(request.app.state.s3_code)
    file = await files_operations_usecase.download(settings.S3_FUNCTION_LOGS_BUCKET,
                                                   f"{user_id}/{function_id}/{log_id}.json")
    return StreamingResponse(file, media_type="application/octet-stream",
                             headers={
                                 "Content-Disposition": f'attachment; filename="{log_id}.json"'
                             })

@user_files_router.get("/runnable-list")
async def runnable_list(project_id: int, path: str, request: Request):
    user_id = request.state.credentials["user_id"]
    return await RunnableListUseCase(request.app.state.s3_code).execute(f"{user_id}/{project_id}/{path}")