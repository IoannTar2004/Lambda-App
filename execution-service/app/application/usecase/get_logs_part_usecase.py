from application.ports.cache_hash_set import CacheHashSet
from application.ports.log_stream import LogStream
from application.utils.redis_formats import logs_key_f


class GetLogsPartUsecase:

    def __init__(self, log_stream: LogStream):
        self.log_stream = log_stream

    async def execute(self, user_id: int, run_id: str, begin: str, end: str):
        logs = await self.log_stream.read(logs_key_f(user_id, run_id), begin, end)
        logs = [{"timestamp": id, "text": text} for id, text in logs]
        return logs