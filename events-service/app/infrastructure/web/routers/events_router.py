from fastapi import APIRouter
from fastapi import Request

from application.usecase.functions_list_usecase import FunctionsListUseCase
from infrastructure.cache.redis import RedisClient
from infrastructure.config.consul import get_service_url
from infrastructure.messaging.httpx_async_request import HttpxAsyncRequest

router = APIRouter(prefix="/api/events", tags=["Events Controller"])


@router.get("/functions-list")
async def functions_list(path: str, request: Request):
    redis_client = RedisClient(request.app.state.redis)
    res = await FunctionsListUseCase(redis_client, HttpxAsyncRequest()).execute(path)
    return res
