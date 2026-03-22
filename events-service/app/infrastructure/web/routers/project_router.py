from typing import Annotated

from fastapi import APIRouter
from pydantic import Field

from application.usecase.projects.create_project_usecase import CreateProjectUsecase
from application.usecase.projects.rollback_project_usecase import RollbackProjectUsecase
from application.usecase.projects.commit_project_usecase import CommitProjectUseCase
from infrastructure.database.sqlalchemy_db_transaction import SqlAlchemyDBTransaction
from infrastructure.messaging.httpx_async_request import HttpxAsyncRequest

project_router = APIRouter(prefix="/api/project", tags=["Project"])


@project_router.post("/create")
async def create_project(project_name: Annotated[str, Field(min_length=3, max_length=64)]):
    async_req = HttpxAsyncRequest()
    db_transaction = SqlAlchemyDBTransaction()
    return await CreateProjectUsecase(async_req, db_transaction).execute(300904, project_name)

@project_router.post("/commit-project")
async def commit_project(project_id: Annotated[int, Field(ge=1)]):
    async_req = HttpxAsyncRequest()
    db_transaction = SqlAlchemyDBTransaction()
    await CommitProjectUseCase(async_req, db_transaction).execute(300904, project_id)
    return {"success": True}

@project_router.delete("/rollback")
async def rollback(project_id: Annotated[int, Field(ge=1)]):
    async_req = HttpxAsyncRequest()
    db_transaction = SqlAlchemyDBTransaction()
    await RollbackProjectUsecase(async_req, db_transaction).execute(300904, project_id)

    return {"success": True}