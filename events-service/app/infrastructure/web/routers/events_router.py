from fastapi import APIRouter, Request

from application.usecase.publish_s3_event_usecase import PublishS3EventUsecase
from infrastructure.database.sqlalchemy_db_transaction import SqlAlchemyDBTransaction

events_router = APIRouter(prefix="/api/events/publish", tags=["Events"])

@events_router.post("/s3")
async def s3(request: Request):
    body = await request.json()
    publish_event_usecase = PublishS3EventUsecase(request.app.state.publisher, SqlAlchemyDBTransaction())
    # await publish_event_usecase.execute(body)
    return {"success": True}