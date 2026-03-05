from fastapi import APIRouter

from infrastructure.messaging.kafka_config import kafka

router = APIRouter(prefix="/api/events", tags=["Events Controller"])


@router.get("/test")
async def test():
    print(kafka.producer.send())
    return {"ok": True}