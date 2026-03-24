import os
import shutil
import time
from pathlib import Path

from infrastructure.config.logger_config import logger


async def dir_cleaner_start(directory: str, interval: int):
    for proj_id in os.listdir(directory):
        proj_dir = os.path.join(directory, proj_id)

        for version in os.listdir(proj_dir):
            version_dir = os.path.join(proj_dir, version)
            last_used = (Path(version_dir) / ".last_used")

            if not os.path.exists(last_used):
                shutil.rmtree(version_dir)
                logger.info(f"Project id: {proj_id}, version: {version} was cleaned.")
                continue

            last_used_time = last_used.stat().st_mtime
            minutes_passed = (time.time() - last_used_time)
            lock_file = Path(version_dir) / ".lock_file"
            if minutes_passed >= interval and not os.path.exists(lock_file):
                shutil.rmtree(version_dir)
                logger.info(f"Project id: {proj_id}, version: {version} was cleaned.")
