from typing import Annotated

from fastapi import APIRouter, Request
from pydantic import Field

from application.usecase.projects.create_project_usecase import CreateProjectUsecase
from application.usecase.projects.get_projects_usecase import GetProjectsUsecase
from application.usecase.projects.rollback_project_usecase import RollbackProjectUsecase
from application.usecase.projects.commit_project_usecase import CommitProjectUseCase
from infrastructure.database.sqlalchemy_db_transaction import SqlAlchemyDBTransaction
from infrastructure.messaging.httpx_async_request import HttpxAsyncRequest
from infrastructure.web.dto.commit_project_dto import CommitProjectDTO
from infrastructure.web.dto.create_project_dto import CreateProjectDto

project_router = APIRouter(prefix="/api/events/project", tags=["Project"])


@project_router.get("/get-project")
async def get_project(project_id: Annotated[int, Field(ge=1)], request: Request):
    user_id = request.state.credentials["user_id"]
    get_projects_usecase = GetProjectsUsecase(SqlAlchemyDBTransaction())
    return await get_projects_usecase.get(user_id, project_id)

@project_router.get("/get-projects")
async def get_projects(request: Request):
    user_id = request.state.credentials["user_id"]
    get_projects_usecase = GetProjectsUsecase(SqlAlchemyDBTransaction())
    return await get_projects_usecase.get_all(user_id)

@project_router.post("/create")
async def create_project(data: CreateProjectDto, request: Request):
    user_id = request.state.credentials["user_id"]
    async_req = HttpxAsyncRequest()
    db_transaction = SqlAlchemyDBTransaction()
    return await CreateProjectUsecase(async_req, db_transaction).execute(user_id, data.project_name)

@project_router.post("/commit-project")
async def commit_project(data: CommitProjectDTO, request: Request):
    user_id = request.state.credentials["user_id"]
    async_req = HttpxAsyncRequest()
    db_transaction = SqlAlchemyDBTransaction()
    await CommitProjectUseCase(async_req, db_transaction).execute(user_id, data.model_dump())
    return {"success": True}

@project_router.delete("/rollback")
async def rollback(project_id: Annotated[int, Field(ge=1)], hard: Annotated[bool, Field(default=False)], request: Request):
    user_id = request.state.credentials["user_id"]
    async_req = HttpxAsyncRequest()
    db_transaction = SqlAlchemyDBTransaction()
    await RollbackProjectUsecase(async_req, db_transaction).execute(user_id, project_id, hard)

    return {"success": True}