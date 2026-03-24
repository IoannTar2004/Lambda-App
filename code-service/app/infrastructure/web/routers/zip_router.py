from fastapi import APIRouter, Request

from application.usecase.commands.delete_functions_command import DeleteArchivesCommand
from application.usecase.commands.delete_version_command import DeleteVersionCommand
from application.usecase.commands.zip_project_command import ZipProjectCommand
from application.usecase.delete_all_archives_usecase import DeleteAllArchivesUsecase
from application.usecase.delete_version_usecase import DeleteVersionUsecase
from infrastructure.web.dto.zip.delete_functions_dto import DeleteArchivesDTO
from infrastructure.web.dto.zip.delete_version_dto import DeleteVersionDto
from infrastructure.web.dto.zip.zip_project_dto import ZipProjectDto
from application.usecase.zip_project_usecase import ZipProjectUsecase
from infrastructure.web.mappers.dto_command_mapper import to_command

zip_router = APIRouter(prefix="/api/zip", tags=["Zip versions"])

@zip_router.post("/zip-project")
async def zip_project(data: ZipProjectDto, request: Request):
    storage = request.app.state.storage
    zip_project_usecase = ZipProjectUsecase(storage)
    await zip_project_usecase.execute(to_command(ZipProjectCommand, data))

    return {"success": True}

@zip_router.delete("/delete-version")
async def delete_version(data: DeleteVersionDto, request: Request):
    storage = request.app.state.storage
    delete_version_usecase = DeleteVersionUsecase(storage)
    await delete_version_usecase.execute(to_command(DeleteVersionCommand, data))

    return {"success": True}

@zip_router.delete("/delete-all-archives")
async def delete_all_archives(data: DeleteArchivesDTO, request: Request):
    storage = request.app.state.storage
    delete_all_archives = DeleteAllArchivesUsecase(storage)
    await delete_all_archives.execute(to_command(DeleteArchivesCommand, data))

    return {"success": True}