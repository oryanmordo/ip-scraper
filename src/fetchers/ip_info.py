from utils.decorators import time_execution, redis_cache
from .base import DataFetcher

class IPInfoFetcher(DataFetcher):
    service_name = "ipinfo"
    api_url = "https://api.ipinfo.io/lite/"
    
    # TODO: on a bigger project this would be pulled from a vault or a secret object
    token = "199a34a5eb0b16"
    headers = {"Authorization": f"Bearer {token}"}

    @time_execution
    @redis_cache(ttl=10)
    async def fetch(self,ip: str):
        return self.service_name, await self._get_data(ip, self.headers)