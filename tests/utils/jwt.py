from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
from test_settings import test_settings


def generate_access_token(
    user_login: str,
    user_role: str,
    user_id: str | None = None,
    ttl: timedelta | None = None,
) -> str:
    if not ttl:
        ttl = timedelta(minutes=60)
    if not user_id:
        user_id = str(uuid4())

    datetime_now = datetime.now(timezone.utc)
    expire = datetime_now + ttl
    access_token_payload = {
        "iss": "Auth service",
        "user_login": user_login,
        "user_id": user_id,
        "user_role": user_role,
        "type": "access",
        "exp": expire,
        "iat": datetime_now,
    }
    encoded_jwt = jwt.encode(
        access_token_payload, test_settings.private_key, algorithm="RS256"
    )
    return encoded_jwt
