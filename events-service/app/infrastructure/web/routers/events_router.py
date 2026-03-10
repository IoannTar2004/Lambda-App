from typing import Annotated
from venv import create

from fastapi import APIRouter, Request
from pydantic import Field

from application.commands.create_function_command import CreateFunctionCommand
from application.commands.update_function_command import UpdateFunctionCommand
from application.usecase.create_function_usecase import CreateFunctionUseCase
from application.usecase.delete_function_usecase import DeleteFunctionUsecase
from application.usecase.update_function_usecase import UpdateFunctionUseCase
from application.usecase.functions_list_usecase import FunctionsListUseCase
from application.usecase.rollback_function_usecase import RollbackFunctionUsecase
from infrastructure.cache.redis import RedisClient
from infrastructure.database.sqlalchemy_db_transaction import SqlAlchemyDBTransaction
from infrastructure.messaging.httpx_async_request import HttpxAsyncRequest
from infrastructure.web.dto.create_function_dto import CreateFunctionDTO
from infrastructure.web.dto.update_function_dto import UpdateFunctionDTO

router = APIRouter(prefix="/api/events", tags=["Events Controller"])


@router.get("/functions-list")
async def functions_list(path: str, request: Request):
    redis_client = RedisClient(request.app.state.cache)
    return await FunctionsListUseCase(redis_client, HttpxAsyncRequest()).execute(path)

@router.post("/create-function")
async def create_function(data: CreateFunctionDTO):
    create_function_command = CreateFunctionCommand(**data.model_dump())
    async_req = HttpxAsyncRequest()
    db_transaction = SqlAlchemyDBTransaction()
    return await CreateFunctionUseCase(async_req, db_transaction).execute(create_function_command)

@router.put("/update-function")
async def update_function(data: UpdateFunctionDTO):
    update_function_command = UpdateFunctionCommand(**data.model_dump())
    async_req = HttpxAsyncRequest()
    db_transaction = SqlAlchemyDBTransaction()
    return await UpdateFunctionUseCase(async_req, db_transaction).execute(update_function_command)

@router.delete("/rollback-function")
async def rollback_function(function_id: Annotated[int, Field(ge=0)]):
    async_req = HttpxAsyncRequest()
    db_transaction = SqlAlchemyDBTransaction()
    await RollbackFunctionUsecase(async_req, db_transaction).execute(function_id)

    return {"success": True}

@router.delete("/delete-function")
async def delete_function(function_id: Annotated[int, Field(ge=0)]):
    async_req = HttpxAsyncRequest()
    db_transaction = SqlAlchemyDBTransaction()
    await DeleteFunctionUsecase(async_req, db_transaction).execute(function_id)

    return {"success": True}