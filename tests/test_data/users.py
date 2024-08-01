from utils.jwt import generate_access_token

ADMIN_JWT_TOKEN = generate_access_token(
    "admin_user",
    "admin",
)
ADMIN_TOKEN_COOKIES = {"access_token": ADMIN_JWT_TOKEN}
