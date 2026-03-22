from fastapi import HTTPException

from application.commands.create_function_command import CreateFunctionCommand
from application.ports.async_request import AsyncRequest
from application.ports.db_transaction import DBTransaction
from application.usecase.specific_functions.specific_function import SpecificFunction
from domain.models.function_handler import FunctionHandler
from domain.models.project import Project
from domain.models.function import Function


class CreateFunctionUseCase:

    def __init__(self, async_req: AsyncRequest, db_transaction: DBTransaction, specific_function: SpecificFunction):
        self.async_req = async_req
        self.db_transaction = db_transaction
        self.specific_function = specific_function

    async def execute(self, user_id: int, data: CreateFunctionCommand):
        async with self.db_transaction as tx:
            project: Project = await tx.get(Project, data.project_id)
            if not project:
                raise HTTPException(status_code=404, detail="Project doesn't exist")
            if project.user_id != user_id:
                raise HTTPException(status_code=403, detail="Project doesn't belong to user")

            function = Function(user_id=user_id,
                                name=data.name,
                                project_version=project.version_number,
                                project_id=data.project_id,
                                language=data.language,
                                )
            function = await tx.insert(function)

            function_handler = FunctionHandler(function_id=function.id,
                                               project_version=project.version_number,
                                               function_path=data.function_path,
                                               function_name=data.function_name,
                                               memory_size=data.memory_size,
                                               timeout=data.timeout,
                                               )
            await tx.insert(function_handler)
            await self.specific_function.create(function.id, data, tx, self.async_req)
            return {
                "function_id": function.id
            }