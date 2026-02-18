import time
from fastapi import APIRouter
from utils.session_holder import PersistentSession

router = APIRouter(tags=["System"])

@router.get("/health")
async def health_check():
    # Check if our shared session is initialized and open
    session_active = (
        PersistentSession.session is not None and
        not PersistentSession.session.closed
    )

    return {
        "status": "ok" if session_active else "degraded",
        "timestamp": time.time(),
        "services": {
            "http_client": "connected" if session_active else "disconnected"
        }
    }