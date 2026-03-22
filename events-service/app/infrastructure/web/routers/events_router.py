import json

from fastapi import APIRouter, Request

from application.usecase.publish_event_usecase import PublishEventsUsecase
from infrastructure.database.sqlalchemy_db_transaction import SqlAlchemyDBTransaction

events_router = APIRouter(prefix="/api/events", tags=["Events"])

@events_router.post("/event")
async def events(request: Request):
    body = await request.json()
    publish_event_usecase = PublishEventsUsecase(request.app.state.publisher, SqlAlchemyDBTransaction())
    await publish_event_usecase.execute(body)
    print(json.dumps(body, indent=4))
    return {"success": True}