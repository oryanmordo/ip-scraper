from abc import abstractmethod, ABC

from utils.Logger import logger

class DataFetcher(ABC):

    api_url = None

    def __init__(self):
        logger.info(f"Initializing {self.__class__.__name__} fetcher")

    @classmethod
    def can_handle(cls, api: str) -> bool:
        return api in cls.api_url

    @classmethod
    def get_fetcher(cls, api: str) -> "DataFetcher":
        for subclass in cls.__subclasses__():
            if subclass.can_handle(api):
                return subclass()
        raise ValueError(f"No fetcher found for api: {api}")

    @abstractmethod
    async def fetch(self, ip: str):
        pass