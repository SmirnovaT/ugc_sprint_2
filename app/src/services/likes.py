from datetime import datetime
from http import HTTPStatus
from functools import lru_cache

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.api.v1.schemas import Like, Pagination
from src.core.logger import ugc_logger
from src.db.mongo import get_mongo_db

class LikeService:
    """Service for interacting with Likes"""

    def __init__(self, mongo_db: AsyncIOMotorDatabase):
        self.mongo_db = mongo_db
        self.collection_name = "films"

    async def get(self, film_id, page_number: int = 1, per_page: int = 50):
        """Get all likes for a film"""

        try:
            film = await self.mongo_db[self.collection_name].find_one(
                {'_id': film_id},)
            print("Film: ", film)
            if film is not None:
                result = film["scores"]#.skip((page_number - 1) * per_page).limit(per_page)
                print("Result: ", result)
                if result:
                    like_list = await result.to_list(length=per_page)
                    likes = [Like(**like) for like in like_list]
                    return [l.dict() for l in likes]
            else:
                return []
        except Exception as exc:
            ugc_logger.error(f"Error while getting likes: {exc}")

            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Error while getting likes")



    async def add(self, like_data):
        """Add like for movie"""

        #like_data = jsonable_encoder(data)
        film_id = like_data.film_id
        user_id = like_data.user_id
        score = like_data.score

        film = await self.mongo_db[self.collection_name].find_one(
            {'_id': film_id}, )
        if film is None:
            film = {"_id": film_id, "average_score": score,
                    "scores": [
                        { "user_id": user_id, "score": score,
                          "created_at": datetime.now()
                          }
                    ]
                    }
        else:
            summ=0
            for like in film["scores"]:
                summ += like["score"]
                if like["user_id"] == user_id:
                    raise HTTPException(
                        status_code=HTTPStatus.CONFLICT,
                        detail=f"Like by user {user_id} for movie {film_id} already exist")
            film["average_score"] = summ/ len(film["scores"])

        try:
            new_data = await self.mongo_db[self.collection_name].insert_one(film)
        except Exception as exc:
            ugc_logger.error(f"Error while adding review by {user_id} for movie {film_id}: {exc}")

            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Error while adding review by {user_id} for movie {film_id}")
        return await self.mongo_db[self.collection_name].find_one({'_id': new_data.inserted_id})

@lru_cache()
def get_like_service():
    return LikeService(get_mongo_db())