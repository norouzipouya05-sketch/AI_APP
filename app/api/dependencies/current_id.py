from uuid import UUID
from typing import Annotated
from starlette import status

from fastapi import Header, HTTPException


from app.core.exceptions import InvalidTokenError
from app.core.security import decode_access_token

async def current_id(
    authorization: Annotated[str, Header(None, alias="Authorization")]
) -> UUID:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not is any authorization."
        )
    token = authorization[7: ]
    try:
        pyload = decode_access_token(token)
        return UUID(pyload["sub"])
    except (InvalidTokenError, ValueError, KeyError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="The token with the key is invalid."
        )
