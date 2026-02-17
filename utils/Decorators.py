import time
from functools import wraps


def time_execution(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time_ns()

        result = await func(*args, **kwargs)

        duration = (time.time_ns() - start_time) // 1_000_000

        return result, duration

    return wrapper