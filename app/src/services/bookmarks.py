from functools import lru_cache
from http import HTTPStatus

import structlog
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
from starlette.responses import JSONResponse

from src.api.v1.schemas import BookmarksForUser, User
from src.db.mongo import get_mongo_db

ugc_logger = structlog.get_logger()

class UserService:
    """Service for interacting with User"""

    def __init__(self, mongo_db: AsyncIOMotorDatabase):
        self.mongo_db = mongo_db
        self.collection_name = "users"
        self.collection: AsyncIOMotorCollection = self.mongo_db[self.collection_name]

    async def add_bookmark(self, user_id: str, film_id: str) -> User:
        """Add bookmark for movie"""

        user_data = await self.check_if_user_exist(user_id)
        if not user_data:
            try:
                await self.mongo_db[self.collection_name].insert_one(
                    {"_id": user_id, "bookmarks": [film_id]}
                )
            except Exception as exc:
                ugc_logger.error(f"Error while adding bookmark for {user_id}: {exc}")

                raise HTTPException(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    detail=f"Error while adding bookmark for {user_id}",
                )
        else:
            try:
                bookmarks = user_data.get("bookmarks")
                if not film_id in bookmarks:
                    bookmarks.append(film_id)

                    await self.mongo_db[self.collection_name].update_one(
                        {"_id": user_id}, {"$set": {"bookmarks": bookmarks}}
                    ),
                else:
                    return JSONResponse(
                        status_code=HTTPStatus.CONFLICT,
                        content="This movie is already in bookmarks",
                    )

            except Exception as exc:
                ugc_logger.error(f"Error while adding bookmark for {user_id}: {exc}")

                raise HTTPException(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    detail=f"Error while adding bookmark for {user_id}",
                )

        return await self.mongo_db[self.collection_name].find_one(
            {"_id": user_id},
        )

    async def delete_bookmark(self, user_id: str, film_id: str) -> None:
        """Remove bookmark"""

        user_data = await self.check_if_user_exist(user_id)
        if not user_data:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"User with id {user_id} doesnt exist",
            )

        current_bookmarks = user_data.get("bookmarks")

        try:
            current_bookmarks.remove(film_id)
        except ValueError:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"No such bookmark for {user_id}",
            )

        try:
            await self.mongo_db[self.collection_name].update_one(
                {"_id": user_id},
                {"$set": {"bookmarks": current_bookmarks}},
            )

        except Exception as exc:
            ugc_logger.error(f"Error while removing bookmark for {user_id}: {exc}")

            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Error while removing bookmark for {user_id}",
            )

    async def get_bookmarks(self, user_id: str) -> BookmarksForUser:
        """Get bookmarks"""

        user_data = await self.check_if_user_exist(user_id)
        if not user_data:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"User with id {user_id} doesnt exist",
            )
        else:
            return await self.mongo_db[self.collection_name].find_one({"_id": user_id})

    async def check_if_user_exist(self, user_id: str) -> dict | None:
        """Check if user exists"""

        return await self.mongo_db[self.collection_name].find_one({"_id": user_id})


@lru_cache()
def get_user_service():
    return UserService(get_mongo_db())
