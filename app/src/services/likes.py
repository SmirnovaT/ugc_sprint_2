from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.core.logger import ugc_logger
from src.api.v1.schemas import Like

class LikeService:
    """Service for interacting with Likes"""

    def __init__(self, mongo_db: AsyncIOMotorDatabase):
        self.mongo_db = mongo_db
        self.collection_name = "reviews"

    async def get(self, film_id, page_number: int = 1, per_page: int = 50):
        """Get all likes for a film"""

        try:
            likes = (self.mongo_db[self.collection_name].find_one(
                {'_id': film_id},
            ).skip((page_number - 1) * per_page).limit(per_page)
                     )
        except Exception as exc:
            ugc_logger.error(f"Error while getting likes: {exc}")

            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Error while getting likes")

        reviews_list = await likes.to_list(length=per_page)
        reviews_from_db = [Like(**like) for like in reviews_list]

        return [r.dict() for r in reviews_from_db]