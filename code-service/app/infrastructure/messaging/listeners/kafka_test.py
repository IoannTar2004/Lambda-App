from infrastructure.messaging.kafka_listener import kafka_listener


@kafka_listener("listdir-requests", group_id="code-service")
async def kafka_test(msg):
    print(msg)