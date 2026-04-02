from typing import Annotated

import jwt
from fastapi import APIRouter, HTTPException, Request
from pydantic import Field
from starlette.websockets import WebSocket

from application.usecase.get_logs_part_usecase import GetLogsPartUsecase
from application.usecase.is_active_function_usecase import IsActiveFunctionUsecase
from infrastructure.cache.redis_connection import redis_connection
from infrastructure.cache.redis_hash_set import RedisHashSet
from infrastructure.cache.redis_log_stream import RedisLogStream
from settings import settings

log_router = APIRouter(prefix="/api/execution/log", tags=["Logging with WebSocket"])

@log_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    token = websocket.query_params.get("token")

    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_SECRET_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Signature has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload["user_id"]
    await websocket.accept()
    redis_client = RedisLogStream(redis_connection.redis).client

    async with redis_client.pubsub() as pubsub:
        await pubsub.subscribe(f"user:{user_id}:logs")

        async for message in pubsub.listen():
            if message["type"] == "message":
                try:
                    await websocket.send_text(message["data"])
                except:
                    break


@log_router.get("/get-logs-part")
async def run_logs(request: Request, run_id: str, begin: Annotated[str, Field()] = "-",
                   end: Annotated[str, Field()] = "+"):
    user_id = request.state.credentials["user_id"]
    redis_log_stream = RedisLogStream(redis_connection.redis)
    get_logs_part_usecase = GetLogsPartUsecase(redis_log_stream)
    return await get_logs_part_usecase.execute(user_id, run_id, begin, end)

@log_router.get("/is-active-function")
async def is_active_function(run_id: str):
    redis_hash_set = RedisHashSet(redis_connection.redis)
    is_active_function_usecase = IsActiveFunctionUsecase(redis_hash_set)
    await is_active_function_usecase.execute(run_id)
    return {"success": True}