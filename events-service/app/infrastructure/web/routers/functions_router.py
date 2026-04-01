from typing import Annotated

from fastapi import APIRouter, Request
from pydantic import Field

from application.commands.create_s3_function_command import CreateS3FunctionCommand
from application.usecase.functions.create_function_usecase import CreateFunctionUseCase
from application.usecase.functions.delete_function_usecase import DeleteFunctionUsecase
from application.usecase.functions.functions_list_usecase import FunctionsListUseCase
from application.usecase.functions.get_functions_usecase import GetFunctionsUsecase
from application.usecase.specific_functions.s3_function_usecase import S3FunctionUsecase
from infrastructure.cache.redis import RedisClient
from infrastructure.database.sqlalchemy_db_transaction import SqlAlchemyDBTransaction
from infrastructure.messaging.httpx_async_request import HttpxAsyncRequest
from infrastructure.web.dto.create_s3_function_dto import CreateS3FunctionDTO

functions_router = APIRouter(prefix="/api/events/functions", tags=["Functions Controller"])


@functions_router.get("/list")
async def list(path: str, request: Request):
    redis_client = RedisClient(request.app.state.cache)
    return await FunctionsListUseCase(redis_client, HttpxAsyncRequest()).execute(path)

@functions_router.get("/get")
async def get(function_id: Annotated[int, Field(ge=1)], request: Request):
    user_id = request.state.credentials["user_id"]
    get_function_usecase = GetFunctionsUsecase(SqlAlchemyDBTransaction())
    return await get_function_usecase.get(user_id, function_id)

@functions_router.get("/get-all")
async def get_all(request: Request):
    user_id = request.state.credentials["user_id"]
    get_function_usecase = GetFunctionsUsecase(SqlAlchemyDBTransaction())
    return await get_function_usecase.get_all(user_id)

@functions_router.post("/create-s3")
async def create_s3_function(data: CreateS3FunctionDTO, request: Request):
    user_id = request.state.credentials["user_id"]
    s3_function_usecase = S3FunctionUsecase(request.app.state.s3_service)
    create_s3_function_command = CreateS3FunctionCommand(**data.model_dump())
    return await (CreateFunctionUseCase(HttpxAsyncRequest(), SqlAlchemyDBTransaction(), s3_function_usecase)
                  .execute(user_id, "S3", create_s3_function_command))

@functions_router.delete("/delete-s3")
async def delete_function(function_id: Annotated[int, Field(ge=1)], request: Request):
    user_id = request.state.credentials["user_id"]
    s3_function_usecase = S3FunctionUsecase(request.app.state.s3_service)
    await DeleteFunctionUsecase(HttpxAsyncRequest(), SqlAlchemyDBTransaction(), s3_function_usecase).execute(function_id)

    return {"success": True}
