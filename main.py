import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
import aiohttp

from utils.Decorators import time_api_response
from utils.SessionHolder import PersistentSession

from fetchers import DataFetcher
from utils.utils import recursive_dict


@asynccontextmanager
async def lifespan(app: FastAPI):
    PersistentSession.session = aiohttp.ClientSession()
    yield
    await PersistentSession.session.close()

app = FastAPI(lifespan=lifespan)

@app.get("/id/{ip}")
@time_api_response
async def osint_ip(ip: str):
    tasks = [data_fetcher().fetch(ip) for data_fetcher in DataFetcher.__subclasses__()]

    if not tasks:
        raise HTTPException(status_code=404, detail="No valid fetchers found")

    all_results = await asyncio.gather(*tasks, return_exceptions=True)

    final_results = recursive_dict()

    final_results["metrics"]["total"]["status"] = "success"

    for item in all_results:
        if isinstance(item, Exception):
            logging.error(f"A task failed: {item}")
            final_results["metrics"]["total"]["status"] = "failed"
            continue

        metric, raw_data, api_status = item

        if api_status == "failed":
            final_results["metrics"]["total"]["status"] = "failed"
        final_results["metrics"].update(metric)
        final_results["raw_data"].update(raw_data)

    logging.info("All tasks completed")
    return final_results
