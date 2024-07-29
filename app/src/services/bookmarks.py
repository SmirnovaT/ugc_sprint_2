from http import HTTPStatus
from functools import lru_cache

from bson.objectid import ObjectId
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.core.logger import ugc_logger
from src.db.mongo import get_mongo_db


class UserService:
    """Service for interacting with User"""

    def __init__(self, mongo_db: AsyncIOMotorDatabase):
        self.mongo_db = mongo_db
        self.collection_name = "users"

    async def add_bookmark(self, user_id, user_data):
        """Add bookmark for movie"""

        is_user_exist = await self.check_if_user_exist(user_id)
        if not is_user_exist:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"User with id {user_id} doesnt exist")

        bookmark_data = jsonable_encoder(user_data)

        try:
            bookmark_result = await self.mongo_db[self.collection_name].update_one(
                {"_id": ObjectId(user_id)}, {"$set": bookmark_data},
            )

        except Exception as exc:
            ugc_logger.error(f"Error while adding bookmark for {user_id}: {exc}")

            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Error while adding bookmark for {user_id}")

        if bookmark_result.modified_count == 1:
            return await self.mongo_db[self.collection_name].find_one(
                {"_id": ObjectId(user_id)},
            )

    async def delete_bookmark(self, user_id, film_id):
        """Remove bookmark"""

        user_data = await self.check_if_user_exist(user_id)
        if not user_data:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"User with id {user_id} doesnt exist")

        current_bookmarks = user_data.get("bookmarks")

        try:
            current_bookmarks.remove(film_id)
        except ValueError:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"No such bookmark for {user_id}")

        try:
            bookmark_result = await self.mongo_db[self.collection_name].update_one(
                {"_id": ObjectId(user_id)}, {"$set": user_data},
            )

        except Exception as exc:
            ugc_logger.error(f"Error while removing bookmark for {user_id}: {exc}")

            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Error while removing bookmark for {user_id}")

    async def check_if_user_exist(self, user_id):
        """Check if user exists"""

        return await self.mongo_db[self.collection_name].find_one({"_id": ObjectId(user_id)})


@lru_cache()
def get_user_service():
    return UserService(get_mongo_db())
