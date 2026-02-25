from abc import abstractmethod, ABC

from utils.logger import logger
from utils.session_holder import PersistentSession


class DataFetcher(ABC):
    service_name = "base"
    api_url = None

    def __init__(self):
        logger.info(f"Initializing {self.__class__.__name__} fetcher")

    @abstractmethod
    async def fetch(self, ip: str):
        pass
    

    async def _get_data(self, endpoint: str, headers: dict = None) -> dict:
        url = f"{self.api_url}{endpoint}"
        session = PersistentSession.session

        try:
            async with session.get(url, headers=headers, timeout=5) as response:
                if not response.ok:
                    logger.error(f"[{self.service_name}] Failed to fetch {endpoint}. Status: {response.status}")
                    return {"error": "Request failed", "code": response.status}

                return await response.json()
        except Exception as e:
            logger.exception(f"[{self.service_name}] Unexpected error fetching {url}: {e}")
            return {"error": "Connection error", "details": str(e)}