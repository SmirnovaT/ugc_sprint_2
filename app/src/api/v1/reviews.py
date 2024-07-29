from typing import List

from fastapi import APIRouter, Depends, Request, status

from src.api.v1.schemas import Review, ReviewFromDB, Pagination
from src.core.constants import PERMISSIONS
from src.services.reviews import ReviewService
from src.services.reviews import get_review_service
from src.utils.jwt_and_roles import check_token_and_role
from src.utils.pagination import Paginator

router = APIRouter()


@router.get(
    '/',
    response_model=List[ReviewFromDB],
    status_code=status.HTTP_200_OK,
    description="Reviews for movies by users",
    response_description="Reviews for movies",
)
async def get_reviews(
        paginator: Paginator = Depends(),
        service: ReviewService = Depends(get_review_service),
) -> List[ReviewFromDB]:
    return await service.get(paginator.page, paginator.per_page)


@router.post(
    '/',
    response_model=ReviewFromDB,
    status_code=status.HTTP_201_CREATED,
    description="Add review for the film",
    response_description="Added review for the film",
)
async def add_review(
        request: Request,
        review: Review,
        service: ReviewService = Depends(get_review_service),
) -> ReviewFromDB:
    # await check_token_and_role(request, PERMISSIONS["can_add_review"])

    return await service.add(review)


@router.put(
    '/{review_id}',
    response_model=ReviewFromDB,
    status_code=status.HTTP_201_CREATED,
    description="Update review for the film",
    response_description="Update user review to the film",
)
async def update_review(
        request: Request,
        review_id: str,
        review: ReviewFromDB,
        service: ReviewService = Depends(get_review_service)
) -> ReviewFromDB:
    # await check_token_and_role(request, PERMISSIONS["can_update_review"])

    return await service.update(review_id, review)


@router.delete(
    '/{review_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    description="Remove review for the film",
    response_description="Removed review for the film",
)
async def remove_review(
        request: Request,
        review_id: str,
        service: ReviewService = Depends(get_review_service)
) -> None:
    # await check_token_and_role(request, PERMISSIONS["can_remove_review"])

    await service.remove(review_id)
