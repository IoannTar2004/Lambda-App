from application.ports.cache import Cache
from application.ports.log_stream import LogStream


class LogStreamingUsecase:

    def __init__(self, cache: Cache, log_stream: LogStream):
        self.cache = cache
        self.log_stream = log_stream

    async def execute(self, user_id: int, run_id: int, log_id: str):

        return await self.log_stream.read()