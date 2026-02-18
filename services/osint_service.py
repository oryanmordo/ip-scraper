import asyncio
from typing import Any, Dict

from fetchers import DataFetcher
from utils.decorators import time_api_response
from utils.logger import logger
from utils.utils import recursive_dict


class OsintService:
    @staticmethod
    @time_api_response
    async def get_ip_report(ip: str) -> Dict[str, Any]:
        tasks = [data_fetcher().fetch(ip) for data_fetcher in DataFetcher.__subclasses__()]

        all_results = await asyncio.gather(*tasks, return_exceptions=True)

        final_results = recursive_dict()

        final_results["metrics"]["total"]["status"] = "success"

        for item in all_results:
            if isinstance(item, Exception):
                logger.error(f"A task failed: {item}")
                final_results["metrics"]["total"]["status"] = "failed"
                continue

            metric, raw_data, api_status = item

            if api_status == "failed":
                final_results["metrics"]["total"]["status"] = "failed"
            final_results["metrics"].update(metric)
            final_results["raw_data"].update(raw_data)

        logger.info("All tasks completed")
        return final_results