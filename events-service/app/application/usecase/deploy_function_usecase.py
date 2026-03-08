from application.commands.deploy_function_command import DeployFunctionCommand
from application.ports.async_request import AsyncRequest
from application.ports.db_transaction import DBTransaction
from infrastructure.database.models import FunctionHeaderModel


class DeployFunctionUseCase:

    def __init__(self, async_req: AsyncRequest, db_transaction: DBTransaction):
        self.async_req = async_req
        self.db_transaction = db_transaction

    async def execute(self, data: DeployFunctionCommand):
        async with self.db_transaction as tx:
            function_header = FunctionHeaderModel(name="dfef", current_version_number=3, user_id=1)
            tx.add(function_header)