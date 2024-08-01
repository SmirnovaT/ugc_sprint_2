from datetime import datetime
from functools import lru_cache
from http import HTTPStatus

from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.api.v1.schemas import (
    Film,
    Like,
    LikeDeleteSchema,
    LikeSchemaIn,
)
from src.core.logger import ugc_logger
from src.db.mongo import get_mongo_db


class LikeService:
    """Service for interacting with Likes"""

    def __init__(self, mongo_db: AsyncIOMotorDatabase):
        self.mongo_db = mongo_db
        self.collection_name = "films"

    async def get(
        self, film_id: str, page_number: int = 1, per_page: int = 50
    ) -> list[Like]:
        """Get all likes for a film"""

        try:
            film = await self.mongo_db[self.collection_name].find_one(
                {"_id": str(film_id)},
            )
            if film is not None:
                start = (page_number - 1) * per_page
                finish = start + per_page
                if finish >= len(film["scores"]) and start == 0:
                    like_list = film["scores"]
                elif finish >= len(film["scores"]):
                    like_list = film["scores"][start:]
                else:
                    like_list = film["scores"][start:finish]
                print("Result: ", like_list)
                if like_list:
                    likes = [Like(**like) for like in like_list]
                    return [l.model_dump() for l in likes]
                else:
                    return []
            else:
                return []
        except Exception as exc:
            ugc_logger.error(f"Error while getting likes: {exc}")

            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Error while getting likes",
            )

    async def add(self, user_id: str, like_data: LikeSchemaIn) -> Film:
        """Add like for movie"""

        film_id = like_data.film_id
        score = like_data.score

        film = await self.mongo_db[self.collection_name].find_one(
            {"_id": film_id},
        )
        if film is None:
            film = {
                "_id": film_id,
                "average_score": score,
                "scores": [
                    {"user_id": user_id, "score": score, "created_at": datetime.now()}
                ],
            }
            try:
                new_data = await self.mongo_db[self.collection_name].insert_one(film)
                return await self.mongo_db[self.collection_name].find_one(
                    {"_id": new_data.inserted_id}
                )
            except Exception as exc:
                ugc_logger.error(
                    f"Error while adding like by {user_id} for movie {film_id}: {exc}"
                )

                raise HTTPException(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    detail=f"Error while updating like by {user_id} for movie {film_id}",
                )
        else:
            summ = 0
            for like in film["scores"]:
                summ += like["score"]
                if like["user_id"] == user_id:
                    raise HTTPException(
                        status_code=HTTPStatus.CONFLICT,
                        detail=f"Like by user {user_id} for movie {film_id} already exist",
                    )
            film["scores"].append(
                {"user_id": user_id, "score": score, "created_at": datetime.now()}
            )
            film["average_score"] = (summ + score) / len(film["scores"])

            try:
                new_data = await self.mongo_db[self.collection_name].replace_one(
                    {"_id": film_id}, film, upsert=True
                )
                return await self.mongo_db[self.collection_name].find_one(
                    {"_id": film_id}
                )
            except Exception as exc:
                ugc_logger.error(
                    f"Error while adding like by {user_id} for movie {film_id}: {exc}"
                )

                raise HTTPException(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    detail=f"Error while adding like by {user_id} for movie {film_id}",
                )

    async def update(self, user_id: str, like_data: LikeSchemaIn) -> Film:
        """Update movie like"""

        film_id = like_data.film_id
        score = like_data.score

        film = await self.mongo_db[self.collection_name].find_one(
            {"_id": film_id},
        )
        if film is None:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Error while updating like by {user_id} for movie {film_id}. Film does not exist",
            )
        else:
            summ = 0
            for like in film["scores"]:
                if like["user_id"] == user_id:
                    like["score"] = score
                    summ += score
                else:
                    summ += like["score"]
            film["average_score"] = summ / len(film["scores"])

            try:
                new_data = await self.mongo_db[self.collection_name].replace_one(
                    {"_id": film_id}, film, upsert=True
                )
                return await self.mongo_db[self.collection_name].find_one(
                    {"_id": film_id}
                )
            except Exception as exc:
                ugc_logger.error(
                    f"Error while adding like by {user_id} for movie {film_id}: {exc}"
                )

                raise HTTPException(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    detail=f"Error while adding like by {user_id} for movie {film_id}",
                )

    async def delete(self, user_id: str, like_data: LikeDeleteSchema) -> Film:
        """Delete like from the movie"""

        film_id = like_data.film_id

        film = await self.mongo_db[self.collection_name].find_one(
            {"_id": film_id},
        )
        if film is None:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Error while updating like by {user_id} for movie {film_id}. Film does not exist",
            )
        else:
            summ = 0
            new_likes_list = []
            for like in film["scores"]:
                if not like["user_id"] == user_id:
                    new_likes_list.append(like)
                    summ += like["score"]
            film["average_score"] = summ / len(new_likes_list)
            film["scores"] = new_likes_list

            try:
                new_data = await self.mongo_db[self.collection_name].replace_one(
                    {"_id": film_id}, film, upsert=True
                )
                return await self.mongo_db[self.collection_name].find_one(
                    {"_id": film_id}
                )
            except Exception as exc:
                ugc_logger.error(
                    f"Error while adding like by {user_id} for movie {film_id}: {exc}"
                )

                raise HTTPException(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    detail=f"Error while adding like by {user_id} for movie {film_id}",
                )


@lru_cache()
def get_like_service() -> LikeService:
    return LikeService(get_mongo_db())
