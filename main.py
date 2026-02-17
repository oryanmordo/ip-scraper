import asyncio
import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
import aiohttp

from utils.Decorators import time_execution
from utils.SessionHolder import PersistentSession

from fetchers import DataFetcher
from utils.utils import recursive_dict


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize the session
    PersistentSession.session = aiohttp.ClientSession()
    yield
    # Shutdown: Close the session
    await PersistentSession.session.close()

app = FastAPI(lifespan=lifespan)

# --- Helper Logic ---
@time_execution
async def fetch_ip_from_data_source(ip: str, api_url: str):
    session = PersistentSession.session
    # Added a timeout so your API doesn't hang forever if the source is slow
    async with session.get(f"{api_url}{ip}", timeout=5) as response:
        # if response.status != 200:
        #     return None
        return await response.json()

# --- Routes ---
@app.get("/")
def read_root():
    return {"message": "hello world"}


@app.get("/id/{ip}")
async def osint_ip(ip: str):  # Changed to 'async def'
    start_time = time.time_ns()
    api_names = [
        "ipinfo",
        "ip-api",
    ]

    tasks = [DataFetcher.get_fetcher(name).fetch(ip) for name in api_names]

    if not tasks:
        raise HTTPException(status_code=404, detail="No valid fetchers found")

    all_results = await asyncio.gather(*tasks, return_exceptions=True)

    duration = (time.time_ns() - start_time) // 1_000_000

    final_results = recursive_dict()

    final_results["metrics"]["total"]["status"] = "success"
    final_results["metrics"]["total"]["time"] = duration

    for item in all_results:
        if isinstance(item, Exception):
            logging.error(f"A task failed: {item}")
            continue

        (identifier, result), duration = item

        final_results["raw_data"][identifier]["response"] = result
        final_results["metrics"][identifier]["time"] = duration

        api_status = "success" if result.get("status") != "failed" else "failed"
        final_results["metrics"][identifier]["status"] = api_status

        logging.info(f'{result.get("status")} -> {api_status} - {identifier} - {result} - {duration}')

    logging.info("All tasks completed")
    logging.info(final_results)
    return final_results
