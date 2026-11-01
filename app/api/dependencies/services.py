from app.core.redis_client import RedisClient
from app.db.deps import get_db

from app.services.auth import AuthService
from app.services.otp import OTPService

from redis import Redis
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

async def get_redis() -> Redis:
    return await RedisClient.get_redis_connect()

async def get_auth_service(db: Annotated[AsyncSession, Depends(get_db)]) -> AuthService:
    return AuthService(db)

async def get_otp_service(db: Annotated[AsyncSession, Depends(get_db)]) -> OTPService:
    return OTPService(db)



