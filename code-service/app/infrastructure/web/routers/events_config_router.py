from fastapi import APIRouter, Request

from application.usecase.commands.events.create_s3_event_command import CreateS3EventCommand
from application.usecase.s3_event_usecase import S3EventUsecase
from infrastructure.storage.async_s3_service import AsyncS3NotificationService
from infrastructure.web.dto.events.create_s3_event_dto import CreateS3EventDto
from infrastructure.web.dto.events.delete_s3_event_dto import DeleteS3EventDto
from infrastructure.web.mappers.dto_command_mapper import to_command

events_config_router = APIRouter(prefix="/api/events-config", tags=["Event configurations"])

@events_config_router.post("/create-s3-event")
async def create_s3_event(data: CreateS3EventDto, request: Request):
    storage_notification = AsyncS3NotificationService(request.app.state.storage)
    create_s3_event_usecase = S3EventUsecase(storage_notification)
    await create_s3_event_usecase.create(to_command(CreateS3EventCommand, data))

    return {"success": True}

@events_config_router.delete("/delete-s3-event")
async def delete_s3_event(data: DeleteS3EventDto, request: Request):
    storage_notification = AsyncS3NotificationService(request.app.state.storage)
    create_s3_event_usecase = S3EventUsecase(storage_notification)
    await create_s3_event_usecase.delete(data.function_id, data.bucket)

    return {"success": True}