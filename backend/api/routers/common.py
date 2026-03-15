from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse

from settings import system_settings

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    Returns status 200 if the app is running.
    """
    return JSONResponse(content={"status": "ok", "config_name" : system_settings.CONFIG_NAME }, status_code=200)