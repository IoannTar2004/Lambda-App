from pydantic import BaseModel, Field, ConfigDict


class DeployFunctionDTO(BaseModel):
    function_name: str = Field(max_length=128)
    handler: str = Field(max_length=128)
    memory_size: int = Field(le=2048)
    timeout: int = Field(le=300)

    model_config = ConfigDict(extra='forbid')

