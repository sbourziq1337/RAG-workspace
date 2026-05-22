from contextlib import asynccontextmanager
from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app_settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(app_settings.MONGODB_URI)
    app.db_client = app.mongo_conn[app_settings.MONGODB_DB_NAME]
    yield
    # Shutdown
    app.mongo_conn.close()

app = FastAPI(lifespan=lifespan)

app.include_router(base.base_router)
app.include_router(data.data_router)





