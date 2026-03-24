from application.usecase.run_function_usecase import RunFunctionUsecase
from infrastructure.messaging.httpx_async_request import HttpxAsyncRequest
from infrastructure.messaging.kafka.kafka import broker


@broker.subscriber("events", max_workers=1)
async def event_consumer(function_meta):
    await RunFunctionUsecase(HttpxAsyncRequest()).execute(function_meta)