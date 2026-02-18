from contextlib import asynccontextmanager

from fastapi import FastAPI
import aiohttp

from routes import ip_routes, health
from utils.session_holder import PersistentSession

@asynccontextmanager
async def lifespan(_: FastAPI):
    PersistentSession.session = aiohttp.ClientSession()
    yield
    await PersistentSession.session.close()

app = FastAPI(lifespan=lifespan)
app.include_router(ip_routes.router)
app.include_router(health.router)