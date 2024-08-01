from fastapi import APIRouter, Depends, status

from src.api.v1.schemas import BookmarksForUser, User
from src.core.constants import PERMISSIONS
from src.services.bookmarks import UserService, get_user_service
from src.utils.jwt_and_roles import (
    AccessTokenPayload,
    CheckRolesDep,
    verify_access_token_dep,
)

router = APIRouter()


@router.post(
    "/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    description="Add user bookmark to the film",
    response_description="Added user bookmark to the film",
    dependencies=[Depends(CheckRolesDep(roles=PERMISSIONS["can_add_bookmark"]))],
)
async def add_bookmark(
    film_id: str,
    service: UserService = Depends(get_user_service),
    access_token: AccessTokenPayload = Depends(verify_access_token_dep),
) -> User:
    return await service.add_bookmark(access_token.user_id, film_id)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Remove bookmark",
    response_description="Bookmark removed",
    dependencies=[Depends(CheckRolesDep(roles=PERMISSIONS["can_delete_bookmark"]))],
)
async def delete_bookmark(
    film_id: str,
    access_token: AccessTokenPayload = Depends(verify_access_token_dep),
    service: UserService = Depends(get_user_service),
) -> None:
    return await service.delete_bookmark(access_token.user_id, film_id)


@router.get(
    "/",
    response_model=BookmarksForUser,
    status_code=status.HTTP_200_OK,
    description="Get bookmarks for user",
    response_description="Received books for the user",
    dependencies=[Depends(CheckRolesDep(roles=PERMISSIONS["can_add_bookmark"]))],
)
async def get_bookmarks(
    service: UserService = Depends(get_user_service),
    access_token: AccessTokenPayload = Depends(verify_access_token_dep),
) -> BookmarksForUser:
    return await service.get_bookmarks(access_token.user_id)
