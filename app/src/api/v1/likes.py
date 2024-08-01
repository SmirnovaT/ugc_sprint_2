from fastapi import APIRouter, Depends, status

from src.api.v1.schemas import (
    Film,
    Like,
    LikeDeleteSchema,
    LikeSchemaIn,
)
from src.core.constants import PERMISSIONS, PermEnum
from src.services.likes import LikeService, get_like_service
from src.utils.jwt_and_roles import (
    AccessTokenPayload,
    CheckRolesDep,
    verify_access_token_dep,
)
from src.utils.pagination import Paginator

router = APIRouter()


@router.get(path="/",
    status_code=status.HTTP_200_OK,
    description="Get all likes for the movie",
)
async def get_likes(
    film_id,
    paginator: Paginator = Depends(),
    service: LikeService = Depends(get_like_service),
) -> list[Like]:
    return await service.get(film_id, paginator.page, paginator.per_page)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    description="Add like the film",
    dependencies=[Depends(CheckRolesDep(roles=PERMISSIONS[PermEnum.CAN_ADD_LIKE]))],
)
async def add_like(
    like: LikeSchemaIn,
    service: LikeService = Depends(get_like_service),
    access_token: AccessTokenPayload = Depends(verify_access_token_dep),
) -> Film:
    return await service.add(access_token.user_id, like)


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    description="Update like of the movie",
    dependencies=[Depends(CheckRolesDep(roles=PERMISSIONS[PermEnum.CAN_UPDATE_LIKE]))],
)
async def update_like(
    like: LikeSchemaIn,
    service: LikeService = Depends(get_like_service),
    access_token: AccessTokenPayload = Depends(verify_access_token_dep),
) -> Film:
    return await service.update(access_token.user_id, like)


@router.delete(
    "/",
    status_code=status.HTTP_200_OK,
    description="Delete like of the movie",
    dependencies=[Depends(CheckRolesDep(roles=PERMISSIONS[PermEnum.CAN_REMOVE_LIKE]))],
)
async def delete_like(
    like: LikeDeleteSchema,
    service: LikeService = Depends(get_like_service),
    access_token: AccessTokenPayload = Depends(verify_access_token_dep),
) -> Film:
    return await service.delete(access_token.user_id, like)
