from fastapi import APIRouter
from fastapi import Request

from application.commands.deploy_function_command import DeployFunctionCommand
from application.usecase.deploy_function_usecase import DeployFunctionUseCase
from application.usecase.functions_list_usecase import FunctionsListUseCase
from infrastructure.cache.redis import RedisClient
from infrastructure.database.sqlalchemy_db_transation import SqlAlchemyDBTransaction
from infrastructure.messaging.httpx_async_request import HttpxAsyncRequest
from infrastructure.web.dto.deploy_function_dto import DeployFunctionDTO

router = APIRouter(prefix="/api/events", tags=["Events Controller"])


@router.get("/functions-list")
async def functions_list(path: str, request: Request):
    redis_client = RedisClient(request.app.state.cache)
    return await FunctionsListUseCase(redis_client, HttpxAsyncRequest()).execute(path)

@router.post("/deploy-function")
async def deploy_function(data: DeployFunctionDTO, request: Request):
    deploy_function_command = DeployFunctionCommand(**data.model_dump())
    async_req = HttpxAsyncRequest()
    db_transaction = SqlAlchemyDBTransaction()
    return await DeployFunctionUseCase(async_req, db_transaction).execute(deploy_function_command)

