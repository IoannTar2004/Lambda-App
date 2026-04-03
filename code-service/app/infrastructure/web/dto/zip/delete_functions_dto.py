from pydantic import BaseModel, Field


class DeleteArchivesDTO(BaseModel):
    user_id: int
    project_id: int