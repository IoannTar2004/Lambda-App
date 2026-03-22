from application.ports.db_transaction import DBTransaction
from application.ports.publisher import Publisher


class PublishEventsUsecase:

    def __init__(self, publisher: Publisher, db_transaction: DBTransaction):
        self.publisher = publisher
        self.db_transaction = db_transaction

    async def execute(self, message):
        async with self.db_transaction as tx:
            function_header = tx
        await self.publisher.publish(message, "events")