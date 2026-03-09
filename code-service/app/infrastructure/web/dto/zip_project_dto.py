from dataclasses import dataclass

from pydantic import Field, BaseModel


@dataclass
class ZipProjectDto(BaseModel):

    user_id: int = Field()
    project_name: str = Field(min_length=3, max_length=32)
    version_number: int = Field(ge=1)