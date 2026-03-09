from fastapi import APIRouter, Request

from application.usecase.commands.zip_project_command import ZipProjectCommand
from infrastructure.web.dto.zip_project_dto import ZipProjectDto
from application.usecase.zip_project_usecase import ZipProjectUsecase
from infrastructure.web.mappers.dto_command_mapper import to_command

zip_router = APIRouter(prefix="/api/zip", tags=["Zip Controller"])

@zip_router.post("/zip-project")
async def zip_project(data: ZipProjectDto, request: Request):
    storage = request.app.state.storage
    zip_project_usecase = ZipProjectUsecase(storage)
    await zip_project_usecase.execute(to_command(ZipProjectCommand, data))

    return {"status": "ok"}