import functools
import json
import time
from functools import wraps

from utils.redis_client import RedisCache


def time_execution(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time_ns()

        identifier, response = await func(*args, **kwargs)

        duration = (time.time_ns() - start_time) // 1_000_000

        raw_status = response.get("st   atus") if isinstance(response, dict) else "failed"
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


def redis_cache(ttl: int = 10):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self, ip: str, *args, **kwargs):
            redis = await RedisCache.get_client()
            # Create a unique key based on the class name and the IP
            cache_key = f"cache:{self.__class__.__name__}:{ip}"

            # 1. Try to get from Redis
            cached_data = await redis.get(cache_key)
            if cached_data:
                # Return the service name (first element) and the data
                return self.service_name, json.loads(cached_data)

            # 2. Run the actual fetch method
            service_name, data = await func(self, ip, *args, **kwargs)

            # 3. Store in Redis
            if data:
                await redis.setex(cache_key, ttl, json.dumps(data))

            return service_name, data

        return wrapper

    return decorator