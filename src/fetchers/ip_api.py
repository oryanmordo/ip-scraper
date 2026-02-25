from utils.decorators import time_execution, redis_cache
from .base import DataFetcher

class IPApiFetcher(DataFetcher):
    service_name = "ip-api"
    api_url = "http://ip-api.com/json/"

    @time_execution
    @redis_cache(ttl=10)
    async def fetch(self,ip: str):
        return self.service_name, await self._get_data(ip)