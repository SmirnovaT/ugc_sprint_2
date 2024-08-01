from fastapi import APIRouter, Depends, status

from src.api.v1.schemas import ReviewFromDB, ReviewIn
from src.core.constants import PERMISSIONS, PermEnum
from src.services.reviews import ReviewService, get_review_service
from src.utils.jwt_and_roles import (
    AccessTokenPayload,
    CheckRolesDep,
    verify_access_token_dep,
)
from src.utils.pagination import Paginator

router = APIRouter()


@router.get(
    "/",
    response_model=list[ReviewFromDB],
    status_code=status.HTTP_200_OK,
    description="Reviews for movies by users",
    response_description="Reviews for movies",
)
async def get_reviews(
    paginator: Paginator = Depends(),
    service: ReviewService = Depends(get_review_service),
) -> list[ReviewFromDB]:
    return await service.get(paginator.page, paginator.per_page)


@router.post(
    "/",
    response_model=ReviewFromDB,
    status_code=status.HTTP_201_CREATED,
    description="Add review for the film",
    response_description="Added review for the film",
    dependencies=[Depends(CheckRolesDep(roles=PERMISSIONS[PermEnum.CAN_ADD_REVIEW]))],
)
async def add_review(
    review: ReviewIn,
    service: ReviewService = Depends(get_review_service),
    access_token: AccessTokenPayload = Depends(verify_access_token_dep),
) -> ReviewFromDB:
    return await service.add(user_id=access_token.user_id, data=review)


@router.put(
    "/{review_id}",
    response_model=ReviewFromDB,
    status_code=status.HTTP_201_CREATED,
    description="Update review for the film",
    response_description="Update user review to the film",
    dependencies=[
        Depends(CheckRolesDep(roles=PERMISSIONS[PermEnum.CAN_UPDATE_REVIEW]))
    ],
)
async def update_review(
    review_id: str,
    review: ReviewFromDB,
    service: ReviewService = Depends(get_review_service),
) -> ReviewFromDB:
    return await service.update(review_id, review)


@router.delete(
    "/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Remove review for the film",
    response_description="Removed review for the film",
    dependencies=[
        Depends(CheckRolesDep(roles=PERMISSIONS[PermEnum.CAN_REMOVE_REVIEW]))
    ],
)
async def remove_review(
    review_id: str,
    service: ReviewService = Depends(get_review_service),
) -> None:
    await service.remove(review_id)
