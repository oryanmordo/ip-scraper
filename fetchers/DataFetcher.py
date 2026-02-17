from abc import abstractmethod, ABC

from utils.Logger import logger

class DataFetcher(ABC):

    api_url = None

    def __init__(self):
        logger.info(f"Initializing {self.__class__.__name__} fetcher")

    @abstractmethod
    async def fetch(self, ip: str):
        pass