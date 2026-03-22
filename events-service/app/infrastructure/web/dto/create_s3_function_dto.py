from pydantic import Field

from infrastructure.web.dto.create_function_dto import CreateFunctionDTO


class CreateS3FunctionDTO(CreateFunctionDTO):
    bucket: str = Field(min_length=3, max_length=32)
    events: list[str] = Field()
    prefix: str = Field(default="")
    suffix: str = Field(default="")

