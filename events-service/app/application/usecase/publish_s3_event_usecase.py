from application.ports.db_transaction import DBTransaction
from application.ports.publisher import Publisher
from domain.models.function import Function
from domain.models.function_handler import FunctionHandler
from domain.models.s3_function import S3Function


class PublishS3EventUsecase:

    def __init__(self, publisher: Publisher, db_transaction: DBTransaction):
        self.publisher = publisher
        self.db_transaction = db_transaction

    async def execute(self, message):
        bucket = message["Records"][0]["s3"]["bucket"]["name"]
        event = message["EventName"]
        key = ''.join(message["Key"].split("/")[1:])
        sql = ("select * from s3_functions "
               "where case "
                    "when prefix != '' then :key like prefix || '%' "
                    "else TRUE "
               "end "
               "and case "
                    "when suffix != '' then :key like '%' || suffix "
                    "else TRUE " 
               "end "
               "and bucket = :bucket and :event = any (events)")

        async with self.db_transaction as tx:
            s3_functions: list[S3Function] = await tx.get_by_query(S3Function, sql,
                                                             bucket=bucket,
                                                             event=event,
                                                             key=key)
            for s3 in s3_functions:
                function : Function = (await tx.get_by_filters(Function, _joins=["handler"], id=s3.id))[0]
                handler : FunctionHandler = function.relations["handler"]
                message_with_metadata = {
                    "user_id": function.user_id,
                    "function_id": function.id,
                    "language": function.language,
                    "project_id": function.project_id,
                    "project_version": handler.project_version,
                    "function_path": handler.function_path,
                    "function_name": handler.function_name,
                    "memory_size": handler.memory_size,
                    "timeout": handler.timeout,
                    "message": message
                }
                await self.publisher.publish(message_with_metadata, "events")