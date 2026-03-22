import asyncio
import json
import subprocess
from pathlib import Path


class RunFunctionUsecase:

    async def execute(self, message):
        loop = asyncio.get_running_loop()
        script_path = Path("./app/application/utils/lambda_run.py")
        module_path = Path("D:/Program Files/pythonProject/lambda_app/test_scripts/test_script.py")
        function = "print_message"
        def run_docker():
            with subprocess.Popen(
                    ["python", script_path, module_path, function, json.dumps(message, indent=4)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding="cp866"
            ) as process:
                for line in process.stdout:
                    print(line.rstrip())
                for line in process.stderr:
                    print(line.rstrip())

        try:
            await asyncio.wait_for(loop.run_in_executor(None, run_docker), timeout=3)
        except asyncio.TimeoutError:
            print("Timeout")
            return