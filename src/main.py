from contextlib import asynccontextmanager

from fastapi import FastAPI
import aiohttp

from routes import ip_routes, health
from utils.redis_client import RedisCache
from utils.session_holder import PersistentSession

@asynccontextmanager
async def lifespan(_: FastAPI):
    PersistentSession.session = aiohttp.ClientSession()
    await RedisCache.get_client()
    yield
    await PersistentSession.session.close()
    await RedisCache.close()

app = FastAPI(lifespan=lifespan)
app.include_router(ip_routes.router)
app.include_router(health.router)