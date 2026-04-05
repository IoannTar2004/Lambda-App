import asyncio
import json
import tempfile
import ast

import httpx
from fastapi import HTTPException

from application.ports.cache import Cache
from infrastructure.config.executor import executor

from application.ports.storage import Storage
from settings import settings


class RunnableListUseCase:

    def __init__(self, storage: Storage):
        self.storage = storage

    async def execute(self, path: str):
        if not self.storage.exists(settings.S3_USER_CODE_BUCKET, path):
            raise HTTPException(status_code=404, detail="File not found")

        with tempfile.TemporaryFile() as tmpfile:
            async for chunk in self.storage.download(settings.S3_USER_CODE_BUCKET, path):
                tmpfile.write(chunk)

            tmpfile.seek(0)
            loop = asyncio.get_running_loop()

            if path.endswith(".py"):
                return await loop.run_in_executor(executor, ast_analyze_functions_python, tmpfile.read())

        return []


def ast_analyze_functions_python(read_bytes: bytes):
    tree = ast.parse(read_bytes)
    functions_list = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            functions_list.append(node.name)

    return functions_list
