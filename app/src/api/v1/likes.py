from fastapi import APIRouter

from src.api.v1.schemas import Like
from src.services.likes import LikeService, get_like_service

router = APIRouter

@router.get("/")
async def get_likes(paginator: Paginator = Depends(),
                    service: LikeService = Depends(get_like_service)) -> list[Like]:
    return await service.get(paginator.page, paginator.per_page)

@router.post()
async def add_like():
    pass

@router.put()
async def update_like():
    pass

@router.delete()
async def delete_like():
    pass