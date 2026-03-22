from dataclasses import dataclass

from application.commands.create_function_command import CreateFunctionCommand


@dataclass
class CreateS3FunctionCommand(CreateFunctionCommand):
    bucket: str
    events: list[str]
    prefix: str
    suffix: str