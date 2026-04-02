from fastapi import HTTPException

from application.utils.redis_formats import run_function_f
from infrastructure.cache.redis_hash_set import RedisHashSet


class IsActiveFunctionUsecase:

    def __init__(self, cache_hash_set: RedisHashSet):
        self.cache_hash_set = cache_hash_set

    async def execute(self, run_id: str):
        is_active = await self.cache_hash_set.contains(run_function_f(), run_id)
        if not is_active:
            raise HTTPException(status_code=404, detail="Function is not active")