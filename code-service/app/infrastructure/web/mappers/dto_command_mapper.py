from pydantic import BaseModel


def to_command(command_class, dto: BaseModel):
    return command_class(**dto.model_dump())