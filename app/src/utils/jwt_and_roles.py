from enum import Enum
from http import HTTPStatus
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import APIKeyCookie
from pydantic import BaseModel, ValidationError

from src.core.config import settings
from src.core.logger import ugc_logger


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class TokenPayload(BaseModel):
    iss: str
    type: TokenType
    iat: int
    exp: int


class AccessTokenPayload(TokenPayload):
    user_id: str
    user_login: str
    user_role: str


cookie_scheme = APIKeyCookie(name="access_token")


async def verify_access_token_dep(
    jwt_token: Annotated[str, Depends(cookie_scheme)],
) -> AccessTokenPayload:
    if not jwt_token:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Access token is missing",
        )
    decoded_token = await validate_token(jwt_token)
    try:
        access_token = AccessTokenPayload(**decoded_token)
    except ValidationError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Access token is invalid",
        )
    return access_token


class CheckRolesDep:
    def __init__(self, roles: list) -> None:
        self.roles = roles

    async def __call__(
        self,
        access_token: AccessTokenPayload = Depends(verify_access_token_dep),
    ) -> None:
        if access_token.user_role not in self.roles:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="User doesn't have required permissions",
            )


async def validate_token(token: str) -> dict:
    """Validates token"""
    try:
        decoded_token: dict[str, str] = jwt.decode(
            jwt=token, key=settings.public_key, algorithms=["RS256"], leeway=30
        )
    except jwt.exceptions.DecodeError as decode_error:
        ugc_logger.error(f"Error while JWT decoding: {decode_error}")
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Access token is invalid",
        )
    except jwt.ExpiredSignatureError:
        ugc_logger.error("Срок действия токена истек")
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Access token is expired",
        )
    except ValueError as err:
        ugc_logger.error(f"Error while JWT decoding: {err}")
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Access token is invalid",
        )

    return decoded_token
