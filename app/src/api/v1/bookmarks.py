from fastapi import APIRouter, Depends, Request, status

from src.api.v1.schemas import User, BookmarksForUser
from src.services.bookmarks import UserService, get_user_service

router = APIRouter()


@router.post(
    "/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    description="Add user bookmark to the film",
    response_description="Added user bookmark to the film",
)
async def add_bookmark(
    request: Request,
    user_id: str,
    film_id: str,
    service: UserService = Depends(get_user_service),
) -> User:
    # await check_token_and_role(request, PERMISSIONS["can_add_bookmark"])

    return await service.add_bookmark(user_id, film_id)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Remove bookmark",
    response_description="Bookmark removed",
)
async def delete_bookmark(
    request: Request,
    user_id: str,
    film_id: str,
    service: UserService = Depends(get_user_service),
) -> None:
    # await check_token_and_role(request, PERMISSIONS["can_delete_bookmark"]))

    return await service.delete_bookmark(user_id, film_id)


@router.get(
    "/{user_id}",
    response_model=BookmarksForUser,
    status_code=status.HTTP_200_OK,
    description="Get bookmarks for user",
    response_description="Received books for the user",
)
async def get_bookmark(
    request: Request,
    user_id: str,
    service: UserService = Depends(get_user_service),
) -> BookmarksForUser:
    # await check_token_and_role(request, PERMISSIONS["can_get_bookmarks"]))

    return await service.get_bookmarks(user_id)
