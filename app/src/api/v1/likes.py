from fastapi import APIRouter, Depends

from src.api.v1.schemas import Like, Like_with_film_id, Film
from src.services.likes import LikeService, get_like_service
from src.utils.pagination import Paginator

router = APIRouter()


@router.get(path="/")
async def get_likes(
    film_id,
    paginator: Paginator = Depends(),
    service: LikeService = Depends(get_like_service),
) -> list[Like]:
    return await service.get(film_id, paginator.page, paginator.per_page)


@router.post("/")
async def add_like(
    like: Like_with_film_id, service: LikeService = Depends(get_like_service)
) -> Film:
    return await service.add(like)


@router.put("/")
async def update_like(
    like: Like_with_film_id, service: LikeService = Depends(get_like_service)
) -> Film:
    return await service.update(like)


@router.delete("/")
async def delete_like(
    like: Like_with_film_id, service: LikeService = Depends(get_like_service)
) -> Film:
    return await service.delete(like)
