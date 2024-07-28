from http import HTTPStatus

import jwt
from fastapi import Request
from fastapi.exceptions import HTTPException

from src.core.config import settings
from src.core.logger import ugc_logger


async def validate_token(token: str) -> dict[str, str]:
    """Validates token"""

    try:
        decoded_token: dict[str, str] = jwt.decode(
            jwt=token,
            key=settings.public_key,
            algorithms=["RS256"],
        )
    except jwt.exceptions.DecodeError as decode_error:
        ugc_logger.error(f"Error while JWT decoding: {decode_error}")
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Неверный токен",
        )
    except jwt.ExpiredSignatureError:
        ugc_logger.error("Срок действия токена истек")
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Срок действия токена истек",
        )
    except ValueError as err:
        ugc_logger.error(f"Error while JWT decoding: {err}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Error while JWT decoding",
        )

    return decoded_token


async def check_token_and_role(request: Request, roles: list) -> None:
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="В cookies отсутствует access token",
        )

    decoded_token = await validate_token(access_token)
    if decoded_token.get("user_role") not in roles:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Нет прав для совершения действия",
        )
