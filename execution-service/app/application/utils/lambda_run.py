import importlib.util
import sys

module_path = sys.argv[1]  # /path/to/file.py
func_name = sys.argv[2]    # имя функции
args = sys.argv[3:]        # остальные аргументы

# загрузка модуля из пути
spec = importlib.util.spec_from_file_location("user_module", module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# вызов функции
func = getattr(module, func_name)
func(*args)