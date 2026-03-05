import asyncio
from functools import wraps
from typing import Coroutine

from aiokafka import AIOKafkaConsumer

from settings import settings


def kafka_listener(*topics: str, group_id: str, enable_auto_commit: bool = False):
    def wrapper(coroutine: Coroutine):
        @wraps(coroutine)
        async def inner(*args, **kwargs):
            print(coroutine.__name__)
            loop = asyncio.get_event_loop()
            consumer = AIOKafkaConsumer(
                *topics,
                loop=loop,
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                enable_auto_commit=enable_auto_commit,
                group_id=group_id
            )
            await consumer.start()
            try:
                async for msg in consumer:
                    await coroutine(msg, *args, **kwargs)
            finally:
                await consumer.stop()

        return inner
    return wrapper