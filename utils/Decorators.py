import time
from functools import wraps

def time_execution(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time_ns()

        identifier, response = await func(*args, **kwargs)

        duration = (time.time_ns() - start_time) // 1_000_000

        raw_status = response.get("status") if isinstance(response, dict) else "failed"
        api_status = "success" if raw_status in ["success", None] else "failed"

        metric = {
            identifier: {
                "time": duration,
                "status": api_status
            }
        }

        raw_data = {
            identifier: {
                "response": response
            }
        }

        return metric, raw_data, api_status

    return wrapper


def time_api_response(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time_ns()

        result = await func(*args, **kwargs)

        duration = (time.time_ns() - start_time) // 1_000_000

        if isinstance(result, dict) or hasattr(result, "__getitem__"):
            result["metrics"]["total"]["time"] = duration

        return result

    return wrapper