from fastapi import HTTPException

from application.ports.db_transaction import DBTransaction
from domain.models.function import Function


class GetExecutionLogsUsecase:

    def __init__(self, db_transaction: DBTransaction):
        self.db_transaction = db_transaction

    async def get_all(self, user_id: int, function_id):
        async with self.db_transaction as tx:
            functions : list[Function] = await tx.get_by_filters(Function, _joins=["logs"], id=function_id)

            if not functions:
                raise HTTPException(status_code=404, detail="Function doesn't exist")

            if functions[0].user_id != user_id:
                raise HTTPException(status_code=403, detail="Functions don't belong to this user")

            return functions[0].relations["logs"]