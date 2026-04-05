import json
import subprocess
from pathlib import Path

from settings import settings


class DocketMounts:

    lambda_path: str | None = None
    archives_path: str | None = None

    @staticmethod
    def set_mounts():
        DocketMounts.lambda_path = get_host_mount_path(settings.LAMBDA_SCRIPT_PATH)
        DocketMounts.archives_path = get_host_mount_path(settings.CODE_ARCHIVES_DIRECTORY)


def get_host_mount_path(container_path: str):
    try:
        result = subprocess.run(
            ["docker", "inspect", "execution-service", "--format", "{{json .Mounts}}"],
            capture_output=True,
            text=True
        )

        mounts = json.loads(result.stdout)

        for mount in mounts:
            if mount["Destination"] == container_path:
                return Path(mount["Source"])

        return None

    except Exception as e:
        print(f"Error: {e}")
        return None