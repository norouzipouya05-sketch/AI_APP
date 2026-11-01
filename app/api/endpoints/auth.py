from fastapi import APIRouter, Depends, HTTPException
from app.schemes.request import (
    RegisterUser,
    LoginRequest,
    LogoutUser,
    RefreshToken,
    )
from app.schemes.response import AuthResponse
from app.services.auth import AuthService
from app.api.dependencies.services import (
    get_auth_service,
    get_redis
)
from app.api.dependencies.current_id import current_id
from app.core.exceptions import(
    CredentialError,
    UserAlreadyExistsError,
    UserNotFoundError,
    InvalidTokenError,
)

from typing import Annotated
from redis.asyncio import Redis
from uuid import UUID

router = APIRouter(prefix="/auth/", tags=["auth"])

@router.post("/register", response_model=AuthResponse)
async def register_user(
    user_data: RegisterUser,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    redis: Annotated[Redis, Depends(get_redis)]
):
    try:
        result = await auth_service.register(user_data, redis)
        return result
    except (CredentialError, UserAlreadyExistsError) as er:
        raise HTTPException(
            status_code=er.status_code, detail=er.default_detail
        )
        
@router.post("/login", response_model=AuthResponse)
async def login_user(
    user_data: LoginRequest,
    login_service: Annotated[AuthService, Depends(get_auth_service)]
):
    try:
        result = await login_service.login_user(user_data)
        return result
    except (CredentialError, UserNotFoundError) as er:
        raise HTTPException(
            status_code=er.status_code, detail=er.default_detail
        )
        
@router.post("/logout")
async def logout_user(
    logout_data: LogoutUser,
    current_id: Annotated[UUID, Depends(current_id)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    try:
        result = await auth_service.Invalid_token(logout_data, current_id)
        return result
    except InvalidTokenError as er:
        raise HTTPException(
            status_code=er.status_code, detail=er.default_detail
        )
        
@router.post("/refresh/token", response_model=AuthResponse)
async def refresh_token(
    refresh_data: RefreshToken,
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    try:
        result = await auth_service.refresh_token(refresh_data)
        return result
    except (UserNotFoundError, InvalidTokenError) as er:
        raise HTTPException(
            status_code=er.status_code, detail=er.default_detail
        )
        
@router.delete("/delete_accont")
async def delete_accont(
    user_id: Annotated[UUID, Depends(current_id)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    try:
        result = await auth_service.delete_accont(user_id)
        return result
    except UserNotFoundError as er:
        raise HTTPException(
            status_code=er.status_code, detail=er.default_detail
        )