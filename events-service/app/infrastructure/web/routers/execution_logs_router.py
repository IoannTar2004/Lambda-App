from fastapi import APIRouter, Request

from application.usecase.execution_logs.get_execution_logs_usecase import GetExecutionLogsUsecase
from infrastructure.database.sqlalchemy_db_transaction import SqlAlchemyDBTransaction

execution_logs_router = APIRouter(prefix="/api/events/execution_logs", tags=["Execution Logs"])

@execution_logs_router.get("/get-all")
async def get_all_execution_logs(function_id: int, request: Request):
    user_id = request.state.credentials["user_id"]
    get_execution_logs_usecase = GetExecutionLogsUsecase(SqlAlchemyDBTransaction())
    return await get_execution_logs_usecase.get_all(user_id, function_id)