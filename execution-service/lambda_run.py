import importlib.util
import sys
import time
import json

def main():
    module_path = sys.argv[1]
    func_name = sys.argv[2]
    args = sys.argv[3:]
    
    spec = importlib.util.spec_from_file_location("user_module", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    func = getattr(module, func_name)
    
    start_time = time.time()
    func(*args)
    execution_time = time.time() - start_time
    
    # Выводим время выполнения
    print(execution_time)

if __name__ == "__main__":
    main()