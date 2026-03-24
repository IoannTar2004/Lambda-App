import asyncio
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import httpx
from fastapi import HTTPException

from application.ports.async_request import AsyncRequest
from settings import settings


class RunFunctionUsecase:

    def __init__(self, async_req: AsyncRequest):
        self.async_req = async_req

    async def execute(self, function_meta):
        target_dir = (Path(settings.CODE_ARCHIVES_DIRECTORY) / str(function_meta["project_id"]) /
                      f"v{function_meta['project_version']}")
        if not os.path.exists(target_dir):
            await self.download_and_unzip_code(target_dir, function_meta)

        last_used = target_dir / ".last_used"
        last_used.touch()

        loop = asyncio.get_running_loop()
        script_path = Path("./app/application/utils/lambda_run.py")
        module_path = target_dir / function_meta["function_path"]
        function_name = function_meta["function_name"]
        def run_docker():
            with subprocess.Popen(
                    ["python", script_path, module_path, function_name, json.dumps(function_meta["message"], indent=4)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding="cp866"
            ) as process:
                for line in process.stdout:
                    print(line.rstrip())
                for line in process.stderr:
                    print(line.rstrip())

        lock_file = target_dir / ".lock_file"
        lock_file.touch()
        try:
            await asyncio.wait_for(loop.run_in_executor(None, run_docker), timeout=function_meta["timeout"])
        except asyncio.TimeoutError:
            print("Timeout")
        os.remove(lock_file)

    async def download_and_unzip_code(self, target_dir, function_meta):
        storage_archive_path = (f"{function_meta['user_id']}/{function_meta['project_id']}/"
                                f"v{function_meta['project_version']}.zip")

        if not os.path.exists(target_dir.parent):
            os.makedirs(target_dir.parent)

        tmpfile = tempfile.NamedTemporaryFile(dir=target_dir.parent, suffix=".zip", delete=False)
        try:
            async for chunk in self.async_req.get_stream("/api/file/download-file", "code-service",
                                                         {"bucket": "code-archives", "path": storage_archive_path}):
                tmpfile.write(chunk)

            tmpfile.flush()
            tmpfile.close()

            shutil.unpack_archive(tmpfile.name, target_dir)

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise HTTPException(status_code=404, detail="File not found")

        finally:
            if os.path.exists(tmpfile.name):
                os.remove(tmpfile.name)