from application.usecase.run_function_usecase import RunFunctionUsecase
from infrastructure.messaging.kafka.kafka import broker


@broker.subscriber("events", max_workers=1)
async def event_consumer(message):
    await RunFunctionUsecase().execute(message)