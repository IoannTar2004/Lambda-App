import asyncio
import json
import tempfile
import ast

import httpx
from fastapi import HTTPException

from application.ports.async_request import AsyncRequest
from application.ports.cache import Cache
from infrastructure.config.executor import executor


class FunctionsListUseCase:

    def __init__(self, cache: Cache, async_req: AsyncRequest):
        self.cache = cache
        self.async_req = async_req

    async def execute(self, path: str):
        functions_list = await self.cache.get(f"functions:" + path)
        if functions_list:
            return json.loads(functions_list)

        with tempfile.TemporaryFile() as tmpfile:
            try:
                async for chunk in self.async_req.get_stream("/api/user-files/download-file", "code-service",
                                                             {"path": path}):
                    tmpfile.write(chunk)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise HTTPException(status_code=404, detail="File not found")

            tmpfile.seek(0)
            loop = asyncio.get_running_loop()

            functions_list = await loop.run_in_executor(executor, ast_analyze_functions, tmpfile.read())
            await self.cache.set(f"functions:" + path, json.dumps(functions_list))

        return functions_list


def ast_analyze_functions(read_bytes: bytes):
    tree = ast.parse(read_bytes)
    functions_list = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            functions_list.append(node.name)

    return functions_list
