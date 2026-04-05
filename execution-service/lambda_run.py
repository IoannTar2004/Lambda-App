import importlib.util
import sys
import time
import traceback


def main():
    module_path = sys.argv[1]
    func_name = sys.argv[2]
    args = sys.argv[3:]
    start_time = time.time()

    try:
        spec = importlib.util.spec_from_file_location("user_module", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        func = getattr(module, func_name)

        func(*args)
    except Exception as e:
        print(traceback.format_exc())
    finally:
        execution_time = time.time() - start_time
        print(execution_time)


    # Выводим время выполнения

if __name__ == "__main__":
    main()