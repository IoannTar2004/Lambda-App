from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from application.commands.add_execution_log_command import AddExecutionLogCommand
from application.ports.db_transaction import DBTransaction
from domain.models.execution_log import ExecutionLog


class AddExecutionLogUsecase:

    def __init__(self, db_transaction: DBTransaction):
        self.db_transaction = db_transaction

    async def execute(self, data: AddExecutionLogCommand):
        async with self.db_transaction as tx:
            execution_log = ExecutionLog(data.id, data.function_id, data.execution_time)

            try:
                await tx.insert(execution_log)
            except IntegrityError:
                raise HTTPException(status_code=404, detail="Function not found")