import redis.asyncio as redis

class RedisCache:
    _client = None

    @classmethod
    async def get_client(cls):
        if cls._client is None:
            # TODO: make the redis url configurable
            cls._client = redis.from_url("redis://localhost:6379", decode_responses=True)
        return cls._client

    @classmethod
    async def close(cls):
        if cls._client:
            await cls._client.close()