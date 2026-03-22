from faststream.kafka import KafkaBroker

from settings import settings

broker = KafkaBroker(settings.KAFKA_BOOTSTRAP_SERVERS)