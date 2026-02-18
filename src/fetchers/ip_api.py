from utils.decorators import time_execution, redis_cache
from utils.session_holder import PersistentSession
from .base import DataFetcher

class IPApiFetcher(DataFetcher):
    service_name = "ip-api"
    api_url = "http://ip-api.com/json/"

    @time_execution
    @redis_cache(ttl=10)
    async def fetch(self,ip: str):
        session = PersistentSession.session
        # Added a timeout so your API doesn't hang forever if the source is slow
        async with session.get(f"{self.api_url}{ip}", timeout=5) as response:
            return self.service_name, await response.json()