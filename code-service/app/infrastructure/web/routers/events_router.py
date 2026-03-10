from fastapi import APIRouter, Request

from application.usecase.commands.events.create_s3_event_command import CreateS3EventCommand
from application.usecase.create_s3_event_usecase import CreateS3EventUsecase
from infrastructure.storage.async_s3_notification import AsyncS3NotificationService
from infrastructure.web.dto.events.create_s3_event_dto import CreateS3EventDto
from infrastructure.web.mappers.dto_command_mapper import to_command

events_router = APIRouter(prefix="/api/events", tags=["Event configurations"])

@events_router.post("/create-s3-event")
async def create_s3_event(data: CreateS3EventDto, request: Request):
    storage_notification = AsyncS3NotificationService(request.app.state.storage)
    create_s3_event_usecase = CreateS3EventUsecase(storage_notification)
    await create_s3_event_usecase.execute(to_command(CreateS3EventCommand, data))

    return {"success": True}