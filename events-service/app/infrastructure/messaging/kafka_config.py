from aiokafka import AIOKafkaProducer
from fastapi import FastAPI

from settings import settings


class KafkaConfig:

    def __init__(self):
        self.producer : AIOKafkaProducer | None = None

    async def producer_start(self, app: FastAPI):
        self.producer = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS)
        await self.producer.start()
        app.state.producer = self.producer

    async def producer_stop(self):
        if self.producer:
            await self.producer.stop()

kafka = KafkaConfig()