from fastapi import FastAPI, APIRouter
from helpers import get_settings
app = FastAPI()

base_router = APIRouter(prefix="/api", tags=["v1"])

@base_router.get("/")
async def root():
    app_settings = get_settings()
    return {"app name": app_settings.APP_NAME,
            "app version": app_settings.APP_VERSION}

app.include_router(base_router)