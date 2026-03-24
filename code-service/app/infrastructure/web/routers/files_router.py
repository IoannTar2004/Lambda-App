import os

from fastapi import APIRouter, UploadFile, Request
from starlette.responses import StreamingResponse

from application.usecase.files_operations_usecase import FilesOperationsUseCase

files_router = APIRouter(prefix="/api/file", tags=["File (Admin and Communication roles only)"])

@files_router.post("/upload-file")
async def upload_file(file: UploadFile, bucket: str, directory: str, request: Request):
    files_operations_usecase = FilesOperationsUseCase(request.app.state.storage, request.app.state.cache)
    await files_operations_usecase.upload(bucket, file, directory)
    return {"success": True}

@files_router.get("/download-file")
async def download_file(bucket: str, path: str, request: Request):
    files_operations_usecase = FilesOperationsUseCase(request.app.state.storage)
    file = await files_operations_usecase.download(bucket, path)
    return StreamingResponse(file, media_type="application/octet-stream",
                             headers={
                                 "Content-Disposition": f'attachment; filename="{os.path.basename(path)}"'
                             })

@files_router.get("/listdir")
async def listdir(bucket: str, path: str, request: Request):
    files_operations_usecase = FilesOperationsUseCase(request.app.state.storage)
    files = await files_operations_usecase.listdir(bucket, path)
    return files

@files_router.delete("/delete-file")
async def delete_file(bucket: str, path: str, request: Request):
    files_operations_usecase = FilesOperationsUseCase(request.app.state.storage)
    await files_operations_usecase.delete(bucket, path)
    return {"success": True}