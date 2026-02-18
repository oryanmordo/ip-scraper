from fastapi import APIRouter

from services.osint_service import OsintService
from utils.decorators import time_api_response

router = APIRouter(prefix="/id", tags=["IP OSINT"])

@router.get("/{ip}")
@time_api_response
async def get_ip_info(ip: str):
    return await OsintService.get_ip_report(ip)