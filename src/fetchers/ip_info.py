from utils.decorators import time_execution, redis_cache
from utils.session_holder import PersistentSession
from .base import DataFetcher

class IPInfoFetcher(DataFetcher):
    service_name = "ipinfo"
    api_url = "https://api.ipinfo.io/lite/"

    @time_execution
    @redis_cache(ttl=10)
    async def fetch(self,ip: str):
        # TODO: on a bigger project this would be pulled from a vault or a secret object
        token = "199a34a5eb0b16"

        headers = {"Authorization": f"Bearer {token}"}

        session = PersistentSession.session
        async with session.get(f"{self.api_url}{ip}",headers=headers, timeout=5) as response:
            return self.service_name, await response.json()