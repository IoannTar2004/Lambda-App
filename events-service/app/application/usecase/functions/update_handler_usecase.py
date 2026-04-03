from fastapi import HTTPException

from application.commands.update_handler_command import UpdateHandlerCommand
from application.ports.db_transaction import DBTransaction
from domain.models.function import Function
from domain.models.function_handler import FunctionHandler


class UpdateHandlerUsecase:

    def __init__(self, db_transaction: DBTransaction):
        self.db_transaction = db_transaction

    async def execute(self, user_id: int, data: UpdateHandlerCommand):
        async with self.db_transaction as tx:
          functions = await tx.get_by_filters(Function, _joins=["handler"], id=data.function_id)
          if not functions:
              raise HTTPException(status_code=404, detail="Function not found")
          function: Function = functions[0]
          if function.user_id != user_id:
              raise HTTPException(status_code=403, detail="Function doesn't belong to this user")

          handler: FunctionHandler = function.relations["handler"]
          handler.function_path = data.handler_path
          handler.function_name = data.handler
          handler.memory_size = data.memory_size
          handler.timeout = data.timeout

          await tx.update(handler)