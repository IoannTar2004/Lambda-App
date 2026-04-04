from application.usecase.run_function_usecase import RunFunctionUsecase
from infrastructure.cache.redis_connection import redis_connection
from infrastructure.cache.redis_hash_set import RedisHashSet
from infrastructure.cache.redis_log_stream import RedisLogStream
from infrastructure.messaging.httpx_async_request import HttpxAsyncRequest
from infrastructure.messaging.kafka.kafka import broker
from infrastructure.messaging.web_socket_manager import websocket_manager


@broker.subscriber("events")
async def event_consumer(function_meta):
    run_function_usecase = RunFunctionUsecase(HttpxAsyncRequest(), websocket_manager,
                                              RedisLogStream(redis_connection.redis), RedisHashSet(redis_connection.redis))

    await run_function_usecase.execute(function_meta)