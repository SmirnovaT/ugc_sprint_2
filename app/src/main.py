from contextlib import asynccontextmanager

import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

from src.api.v1 import bookmarks, reviews, likes
from src.core.config import settings
from src.db import mongo

sentry_sdk.init(
    dsn=settings.sentry_sdk_dsn,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    mongo.mongo = AsyncIOMotorClient(settings.mongo.url)
    yield


app = FastAPI(
    version="0.0.1",
    title=settings.project_name,
    description="UGC service for Online cinema",
    docs_url="/ugc/api/openapi",
    openapi_url="/ugc/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    contact={
        "name": "Amazing python team",
        "email": "amazaingpythonteam@fake.com",
    },
)

app.include_router(reviews.router, prefix="/ugc/v1/reviews", tags=["reviews"])
app.include_router(likes.router, prefix="/ugc/v1/likes", tags=["likes"])
app.include_router(bookmarks.router, prefix="/ugc/v1/bookmarks", tags=["bookmark"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.default_host,
        port=settings.default_port,
        reload=True,
    )
