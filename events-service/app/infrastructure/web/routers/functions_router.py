from typing import Annotated

from fastapi import APIRouter, Request
from pydantic import Field

from application.commands.create_s3_function_command import CreateS3FunctionCommand
from application.commands.update_handler_command import UpdateHandlerCommand
from application.usecase.functions.create_function_usecase import CreateFunctionUseCase
from application.usecase.functions.delete_function_usecase import DeleteFunctionUsecase
from application.usecase.functions.get_functions_usecase import GetFunctionsUsecase
from application.usecase.functions.update_handler_usecase import UpdateHandlerUsecase
from application.usecase.specific_functions.s3_function_usecase import S3FunctionUsecase
from infrastructure.database.sqlalchemy_db_transaction import SqlAlchemyDBTransaction
from infrastructure.messaging.httpx_async_request import HttpxAsyncRequest
from infrastructure.web.dto.create_s3_function_dto import CreateS3FunctionDTO
from infrastructure.web.dto.update_handler_dto import UpdateHandlerDTO
from infrastructure.web.mappers.dto_command_mapper import to_command

functions_router = APIRouter(prefix="/api/events/functions", tags=["Functions Controller"])


@functions_router.get("/get")
async def get(function_id: Annotated[int, Field(ge=1)], request: Request):
    user_id = request.state.credentials["user_id"]
    get_function_usecase = GetFunctionsUsecase(SqlAlchemyDBTransaction())
    return await get_function_usecase.get(user_id, function_id)

@functions_router.get("/get-all")
async def get_all(project_id: int, request: Request):
    user_id = request.state.credentials["user_id"]
    get_function_usecase = GetFunctionsUsecase(SqlAlchemyDBTransaction())
    return await get_function_usecase.get_all(user_id, project_id)

@functions_router.post("/create-S3")
async def create_s3_function(data: CreateS3FunctionDTO, request: Request):
    user_id = request.state.credentials["user_id"]
    s3_function_usecase = S3FunctionUsecase(request.app.state.s3_service)
    create_s3_function_command = CreateS3FunctionCommand(**data.model_dump())
    return await (CreateFunctionUseCase(HttpxAsyncRequest(), SqlAlchemyDBTransaction(), s3_function_usecase)
                  .execute(user_id, "S3", create_s3_function_command))

@functions_router.delete("/delete-S3")
async def delete_s3_function(function_id: Annotated[int, Field(ge=1)], request: Request):
    user_id = request.state.credentials["user_id"]
    s3_function_usecase = S3FunctionUsecase(request.app.state.s3_service)
    await (DeleteFunctionUsecase(HttpxAsyncRequest(), SqlAlchemyDBTransaction(), s3_function_usecase)
           .execute(user_id, function_id))

    return {"success": True}

@functions_router.patch("/update-handler")
async def update_handler(data: UpdateHandlerDTO, request: Request):
    user_id = request.state.credentials["user_id"]
    update_handler_usecase = UpdateHandlerUsecase(SqlAlchemyDBTransaction())
    await update_handler_usecase.execute(user_id, to_command(UpdateHandlerCommand, data))
    return {"success": True}