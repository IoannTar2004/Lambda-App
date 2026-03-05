import tempfile
import ast

from application.ports.async_request import AsyncRequest
from application.ports.cache import Cache


class FunctionsListUseCase:

    def __init__(self, cache: Cache, async_req: AsyncRequest):
        self.cache = cache
        self.async_req = async_req

    async def execute(self, path: str):
        functions_list = await self.cache.get(f"functions:300904:" + path)
        if functions_list:
            return functions_list["Functions"]

        with tempfile.TemporaryFile() as tmpfile:
            async for chunk in self.async_req.get_stream("/api/code/download-file", "code-service",
                                                         {"path": path}):
                tmpfile.write(chunk)

            tmpfile.seek(0)
            return self.__ast_analyze_functions(tmpfile.read())

    def __ast_analyze_functions(self, read_bytes: bytes):
        tree = ast.parse(read_bytes)
        functions_list = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                functions_list.append(node.name)

        return functions_list
