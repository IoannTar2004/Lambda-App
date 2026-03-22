from faststream.kafka import KafkaBroker

from application.ports.publisher import Publisher

class Kafka(Publisher):
    def __init__(self, bootstrap_servers):
        self.broker = KafkaBroker(bootstrap_servers)

    async def publish(self, message, topic: str):
        await self.broker.publish(message, topic)