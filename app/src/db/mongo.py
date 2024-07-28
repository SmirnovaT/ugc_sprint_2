from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient

mongo: Optional[AsyncIOMotorClient] = None


def get_mongo_db():
    return mongo.ugc
