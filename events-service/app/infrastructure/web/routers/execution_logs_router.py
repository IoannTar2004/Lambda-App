from fastapi import APIRouter, Request

from application.commands.add_execution_log_command import AddExecutionLogCommand
from application.usecase.execution_logs.add_execution_log_usecase import AddExecutionLogUsecase
from application.usecase.execution_logs.get_execution_logs_usecase import GetExecutionLogsUsecase
from infrastructure.database.sqlalchemy_db_transaction import SqlAlchemyDBTransaction
from infrastructure.web.dto.add_execution_log_dto import AddExecutionLogDTO
from infrastructure.web.mappers.dto_command_mapper import to_command

execution_logs_router = APIRouter(prefix="/api/events/execution_logs", tags=["Execution Logs"])

@execution_logs_router.get("/get-all")
async def get_all_execution_logs(function_id: int, request: Request):
    user_id = request.state.credentials["user_id"]
    get_execution_logs_usecase = GetExecutionLogsUsecase(SqlAlchemyDBTransaction())
    return await get_execution_logs_usecase.get_all(user_id, function_id)

@execution_logs_router.post("/add-execution-log")
async def add_execution_log(data: AddExecutionLogDTO):
    add_execution_log_usecase = AddExecutionLogUsecase(SqlAlchemyDBTransaction())
    await add_execution_log_usecase.execute(to_command(AddExecutionLogCommand, data))
    return {"success": True}