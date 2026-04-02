import asyncio
import io
import json
import os
import shutil
import subprocess
import tempfile
import time
import uuid
from pathlib import Path

import httpx
from fastapi import HTTPException

from application.ports.async_request import AsyncRequest
from application.ports.cache_hash_set import CacheHashSet
from application.ports.log_stream import LogStream
from application.ports.socket import Socket
from application.utils.redis_formats import run_function_f, logs_key_f, pubsub_key_f
from infrastructure.config.logger_config import logger
from settings import settings


class RunFunctionUsecase:

    def __init__(self, async_req: AsyncRequest, socket: Socket, log_stream: LogStream, cache: CacheHashSet):
        self.async_req = async_req
        self.socket = socket
        self.log_stream = log_stream
        self.cache = cache

    async def execute(self, function_meta):
        project_id = function_meta["project_id"]
        function_id = function_meta["function_id"]
        user_id = function_meta["user_id"]
        script_path = Path(settings.LAMBDA_SCRIPT_PATH)
        function_name = function_meta["function_name"]

        target_dir = (Path(settings.CODE_ARCHIVES_DIRECTORY) / str(project_id) /
                      f"v{function_meta['project_version']}")
        if not os.path.exists(target_dir):
            await self._download_and_unzip_code(target_dir, function_meta)

        last_used = target_dir / ".last_used"
        last_used.touch()

        loop = asyncio.get_running_loop()
        run_id = uuid.uuid4().hex
        process = None
        container_name = f"{user_id}_{run_id}"

        await self.cache.add(run_function_f(), run_id)
        start_time = time.time()
        def run_docker():
            nonlocal process
            command = self._get_docker_command(container_name, script_path, target_dir, function_meta["function_path"],
                                               function_name, json.dumps(function_meta["message"]),
                                               environment=function_meta["environment"])
            process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding="utf-8"
            )
            future = asyncio.run_coroutine_threadsafe(self._stream_prints(process, user_id, run_id, start_time), loop)
            process.wait()
            future.result()

        lock = target_dir / ".lock_file"
        lock.touch()

        try:
            await asyncio.wait_for(loop.run_in_executor(None, run_docker), timeout=function_meta["timeout"])
        except asyncio.TimeoutError:
            logger.info(f"Function {run_id} timed out")
            await self._kill_docker_container(loop, container_name)

        await self._flush_logs(user_id, function_id, run_id, start_time)
        os.remove(lock)


    async def _download_and_unzip_code(self, target_dir, function_meta):
        storage_archive_path = (f"{function_meta['user_id']}/{function_meta['project_id']}/"
                                f"v{function_meta['project_version']}.zip")

        if not os.path.exists(target_dir.parent):
            os.makedirs(target_dir.parent)

        tmpfile = tempfile.NamedTemporaryFile(dir=target_dir.parent, suffix=".zip", delete=False)
        try:
            async for chunk in self.async_req.get_stream(
                    "/api/code/file/download-file",
                    "code-service",
                    params={"bucket": "code-archives", "path": storage_archive_path}):
                tmpfile.write(chunk)

            tmpfile.flush()
            tmpfile.close()

            shutil.unpack_archive(tmpfile.name, target_dir)

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise HTTPException(status_code=404, detail="File not found")

        finally:
            tmpfile.close()
            if os.path.exists(tmpfile.name):
                os.remove(tmpfile.name)

    def _get_docker_command(self, name, script_path, target_dir, function_path, function_name,
                            *args, environment :str = "python"):
        if environment == "Python 3":
            return [
                "docker", "run",
                "--name", name,
                "--rm", "--read-only",
                "-e", "PYTHONUNBUFFERED=1",
                "--tmpfs", "/mnt/usr:size=64M,mode=1777",
                "-v", f"{script_path}:/usr/lambda_run.py",
                "-v", f"{target_dir}:/usr/src",
                "-w", "/usr/src",
                "python:3", "python", "-u", "/usr/lambda_run.py",
                function_path, function_name, *args
            ]

        return []

    async def _stream_prints(self, process, user_id, run_id, start_time):
        for line in iter(process.stdout.readline, ""):
            message = {"id": run_id, "start_time": start_time, "text": line.rstrip(), "type": "log"}
            id = await self.log_stream.add(logs_key_f(user_id, run_id), message, 30)
            message["timestamp"] = id
            await self.log_stream.publish(pubsub_key_f(user_id), json.dumps(message))

    async def _kill_docker_container(self, loop, container_name):
        await loop.run_in_executor(
            None,
            lambda: subprocess.run(
                ["docker", "kill", container_name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        )

    async def _flush_logs(self, user_id, function_id, run_id, start_time):
        logs = await self.log_stream.read(logs_key_f(user_id, run_id))
        logs = [{"timestamp": id, "text": text["text"]} for id, text in logs]
        execution_time = logs[-1]["text"]
        logs = logs[:-1]

        last_message = json.dumps({"type": "stop", "start_time": start_time, "id": run_id, "text": execution_time})
        await self.log_stream.publish(pubsub_key_f(user_id), last_message)

        if user_id in self.socket.get_connections():
            await self.socket.send_json(user_id, {"id": -1, "run_id": run_id, "text": execution_time})

        file_obj = io.BytesIO(json.dumps(logs, ensure_ascii=False).encode("utf-8"))
        file_obj.seek(0)
        await self.cache.get(run_function_f())
        await self.cache.remove(run_function_f(), run_id)
        await self.cache.get(run_function_f())

        await self.async_req.post("/api/code/file/upload-file", "code-service", data={
            "bucket": "function-logs",
            "directory": f"{user_id}/{function_id}",
        }, files={
            "file": (run_id + ".json", file_obj, "application/json")
        })

        await self.async_req.post("/api/events/execution_logs/add-execution-log", "events-service", json={
            "id": run_id,
            "function_id": function_id,
            "execution_time": execution_time
        })

