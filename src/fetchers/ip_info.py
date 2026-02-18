from cache import AsyncTTL

from utils.decorators import time_execution
from utils.session_holder import PersistentSession
from .base import DataFetcher

class IPInfoFetcher(DataFetcher):
    api_url = "https://api.ipinfo.io/lite/"

    @time_execution
    @AsyncTTL(time_to_live=10)
    async def fetch(self,ip: str):
        token = "199a34a5eb0b16"

        headers = {"Authorization": f"Bearer {token}"}

        session = PersistentSession.session
        async with session.get(f"{self.api_url}{ip}",headers=headers, timeout=5) as response:
            return "ipinfo", await response.json()