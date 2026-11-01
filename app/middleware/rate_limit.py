from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import get_settings
from app.core.rate_limit import RateLimiter
from app.core.redis_client import get_redis
from app.core.security import decode_token_safely

settings = get_settings()


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        identifier = await self._get_identifier(request)
        is_authenticated = identifier.startswith("user:")

        limit = (
            settings.rate_limit_authenticated
            if is_authenticated
            else settings.rate_limit_unauthenticated
        )

        window: int = settings.rate_limit_per_min
        redis = await get_redis()
        limiter = RateLimiter(redis=redis)

        allowed, headers = await limiter.check_request(identifier, limit, window)

        if not allowed:
            raise HTTPException(
                status_code=429, detail="Too many requests", headers=headers
            )

        response = await call_next(request)

        for key, value in headers.items():
            response.headers[key] = value
        response.headers["RateLimit-Scope"] = "user" if is_authenticated else "ip"

        return response

    async def _get_identifier(self, request: Request) -> str:
        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]
            payload = decode_token_safely(token)
            if payload and "sub" in payload:
                return f"user:{payload['sub']}"

        return f"ip:{request.client.host}"
