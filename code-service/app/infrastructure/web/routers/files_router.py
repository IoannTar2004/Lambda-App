import os

from fastapi import APIRouter, UploadFile, Request
from fastapi.params import Form
from starlette.responses import StreamingResponse

from application.usecase.delete_all_usecase import DeleteAllUsecase
from application.usecase.files_operations_usecase import FilesOperationsUseCase

files_router = APIRouter(prefix="/api/code/file", tags=["File (Admin and Communication roles only)"])

@files_router.post("/upload-file")
async def upload_file(request: Request, file: UploadFile,
                      bucket: str = Form(max_length=64), directory: str = Form(max_length=256)):
    files_operations_usecase = FilesOperationsUseCase(request.app.state.s3_code)
    await files_operations_usecase.upload(bucket, file, directory)
    return {"success": True}

@files_router.get("/download-file")
async def download_file(bucket: str, path: str, request: Request):
    files_operations_usecase = FilesOperationsUseCase(request.app.state.s3_code)
    file = await files_operations_usecase.download(bucket, path)
    return StreamingResponse(file, media_type="application/octet-stream",
                             headers={
                                 "Content-Disposition": f'attachment; filename="{os.path.basename(path)}"'
                             })

@files_router.get("/listdir")
async def listdir(bucket: str, path: str, request: Request):
    files_operations_usecase = FilesOperationsUseCase(request.app.state.s3_code)
    files = await files_operations_usecase.listdir(bucket, path)
    return files

@files_router.get("/listdir-all")
async def listdir_all(request: Request, bucket: str, path: str = ""):
    files_operations_usecase = FilesOperationsUseCase(request.app.state.s3_code)
    files = await files_operations_usecase.listdir_all(bucket, path)
    return files

@files_router.delete("/delete-file")
async def delete_file(bucket: str, path: list[str], request: Request):
    files_operations_usecase = FilesOperationsUseCase(request.app.state.s3_code)
    await files_operations_usecase.delete(bucket, path)
    return {"success": True}

@files_router.delete("/delete-all")
async def delete_all(request: Request, bucket: str, path: str = ""):
    storage = request.app.state.s3_code
    delete_all_usecase = DeleteAllUsecase(storage)
    await delete_all_usecase.execute(bucket, path)

    return {"success": True}