def pubsub_key_f(user_id):
    return f"user:{user_id}:logs"


def logs_key_f(user_id, run_id):
    return f"logs:{user_id}:{run_id}"


def run_function_f():
    return f"run_functions"