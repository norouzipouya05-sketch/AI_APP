import jwt
from jwt import PyJWKError

from datetime import datetime, timedelta, timezone
from uuid import UUID

from app.core.config import get_settings
from app.core.exceptions import InvalidTokenError

settings = get_settings()

def create_token(subject: str, token_type: str, expires: timedelta) -> str:
    now = datetime.now(timezone.utc)
    pyload = {
        "sub": subject,
        "type": token_type,
        "iat": int(now.timestamp()),
        "exp": int((now + expires).timestamp())
    }
    token = jwt.encode(pyload, settings.secret_key, algorithm=settings.jwt_algorithm)
    return token

def create_access_token(user_id: UUID):
    return create_token(
        str(user_id),
        "access",
        timedelta(minutes=settings.access_token_expire)
    )
    
def create_refresh_token(user_id: UUID):
    return (
        str(user_id),
        "refresh",
        timedelta(days=settings.refresh_token_expire)
    )
    
def decode_token(token: str) -> dict:
    try:
        pyload = jwt.decode(token, settings.secret_key, settings.jwt_algorithm)
        return pyload
    except PyJWKError as er:
        raise InvalidTokenError("invalid or expired token") from er
    
def decode_access_token(token: str) -> dict:
    pyload = decode_token(token)
    if pyload.get("type") != "access":
        raise InvalidTokenError("this is not access token")
    return pyload

def decode_refresh_token(token: str) -> dict:
    pyload = decode_token(token)
    if pyload.get("type") != "refresh":
        raise InvalidTokenError("this is not refresh token")
    return pyload

def decode_token_safely(token: str) -> dict | None:
    try:
        return decode_token(token)
    except InvalidTokenError:
        return None
