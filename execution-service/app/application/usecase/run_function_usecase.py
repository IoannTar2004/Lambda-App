import asyncio
import io
import json
import os
import shutil
import subprocess
import tempfile
import threading
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
        print("ok")
        revision_id = function_meta["revision_id"]
        project_id = function_meta["project_id"]
        function_id = function_meta["function_id"]
        user_id = function_meta["user_id"]
        script_path = Path(settings.LAMBDA_SCRIPT_PATH)
        function_name = function_meta["function_name"]

        target_dir = Path(settings.CODE_ARCHIVES_DIRECTORY) / str(project_id) / str(revision_id)
        if not os.path.exists(target_dir):
            await self._download_and_unzip_code(target_dir, function_meta)

        last_used = target_dir / ".last_used"
        last_used.touch()

        run_id = uuid.uuid4().hex
        process: subprocess.Popen | None = None
        container_name = f"{user_id}_{run_id}"

        log_queue = asyncio.Queue(maxsize=1000)

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

            for line in iter(process.stdout.readline, ''):
                if not line:
                    break

                msg = {
                    "id": run_id,
                    "start_time": start_time,
                    "text": line.rstrip(),
                    "type": "log",
                    "function_id": function_id
                }
                try:
                    log_queue.put_nowait(msg)
                except asyncio.QueueFull:
                    logger.warning(f"Log queue full for {run_id}, dropping line")

            process.stdout.close()
            process.wait()
            log_queue.put_nowait(None)

        lock = target_dir / (".lock_file" + run_id)
        lock.touch()

        thread = threading.Thread(target=run_docker, daemon=True)
        thread.start()

        writer_task = asyncio.create_task(self._stream_prints(log_queue, user_id, run_id))
        try:
            await asyncio.wait_for(
                asyncio.to_thread(thread.join),
                timeout=function_meta["timeout"]
            )

            await log_queue.join()
            await writer_task

            await self._flush_logs(user_id, function_id, run_id, start_time)

        except asyncio.TimeoutError:
            logger.info(f"Function {run_id} timed out")
            if process and process.poll() is None:
                self._kill_docker_container(container_name)

            await asyncio.sleep(0.2)
            if thread.is_alive():
                thread.join(timeout=1.0)

            writer_task.cancel()
            await self._flush_logs(user_id, function_id, run_id, start_time, function_meta["timeout"])

        os.remove(lock)


    async def _download_and_unzip_code(self, target_dir, function_meta):
        storage_archive_path = (f"{function_meta['user_id']}/{function_meta['project_id']}/"
                                f"{function_meta['revision_id']}.zip")

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

    async def _stream_prints(self, log_queue, user_id, run_id):
        while True:
            msg = await log_queue.get()

            if msg is None:
                log_queue.task_done()
                break

            try:
                msg_id = await self.log_stream.add(logs_key_f(user_id, run_id), msg, 30)
                msg["timestamp"] = msg_id
                await self.log_stream.publish(pubsub_key_f(user_id), json.dumps(msg))
            except Exception as e:
                logger.error(f"Error sending log: {e}")

            log_queue.task_done()

    def _kill_docker_container(self, container_name):
        try:
            subprocess.Popen(
                ["docker", "kill", container_name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception as e:
            pass

    async def _flush_logs(self, user_id, function_id, run_id, start_time, timeout=None):
        logs = await self.log_stream.read(logs_key_f(user_id, run_id))
        logs = [{"timestamp": id, "text": text["text"]} for id, text in logs]
        execution_time = logs[-1]["text"] if not timeout else timeout
        logs = logs[:-1]

        last_message = json.dumps({
            "type": "stop",
            "start_time": start_time,
            "id": run_id, "text": execution_time,
            "function_id": function_id
        })
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

