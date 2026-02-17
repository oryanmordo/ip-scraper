from cache import AsyncTTL

from utils.Decorators import time_execution
from utils.SessionHolder import PersistentSession
from .DataFetcher import DataFetcher

class IPApiFetcher(DataFetcher):
    api_url = "http://ip-api.com/json/"

    @time_execution
    @AsyncTTL(time_to_live=5)
    async def fetch(self,ip: str):
        session = PersistentSession.session
        # Added a timeout so your API doesn't hang forever if the source is slow
        async with session.get(f"{self.api_url}{ip}", timeout=5) as response:
            return "ip-api", await response.json()