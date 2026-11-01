from app.repository.user import UserRepositories
from app.repository.token import TokenRepository
from app.schemes.request import (
    LoginRequest,
    RegisterUser,
    LogoutUser,
    RefreshToken,
)
from app.core.exceptions import(
    CredentialError,
    UserAlreadyExistsError,
    UserNotFoundError,
    InvalidTokenError,
)
from app.core.config import get_settings
from app.core.security import ( 
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    )

from typing import Any
from pwdlib import PasswordHash
from uuid import UUID
import httpx
import pyotp

from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

settings = get_settings()

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self._user_repo = UserRepositories(db)
        self._token_repo = TokenRepository(db)
        self._hasher = PasswordHash.recommended()
        
    async def user_registration_review(self, login_data: LoginRequest) -> Any | None:
        email = getattr(login_data, "email", None)
        phone = getattr(login_data, "phone", None)
        
        if email is not None:
            return await self._user_repo.get_user_by_email(email)
        if phone is not None:
            return await self._user_repo.get_user_by_phone(phone)
        return None
    
    async def register(self, register_data: RegisterUser, redis: Redis) -> dict:
        challenge_token = getattr(register_data, "challenge_token", None)
        email = getattr(register_data, "email", None)
        phone = getattr(register_data, "phone", None)
        password = getattr(register_data, "password", None)
        
        if not challenge_token:
            raise CredentialError("No challenge token.")
        
        if not any([email, phone]):
            raise CredentialError("No email and phone.")
        
        secret = await redis.get(f"otp verify:{phone}")
        
        if isinstance(secret, bytes):
            secret = secret.decode()
            
        if not secret:
            raise CredentialError("The secret code either does not exist or has expired.")
        
        stored_challenge_token = pyotp.TOTP(secret, interval=settings.otp_ttl_sec, digits=6)
        
        if not stored_challenge_token.verify(str(challenge_token), valid_window=1):
            raise CredentialError("The OTP has expired.")
        
        await redis.delete(f"otp verify:{phone}")
        
        if not email and await self._user_repo.exists_by_email(email):
            raise UserAlreadyExistsError("A user with this email has already registered.")
        
        if not phone and self._user_repo.exists_by_phone(phone):
            raise UserAlreadyExistsError("A user with this phone has already registered.")
        
        user_data = {
            "email": email,
            "phone": phone,
            "password": self._hasher.hash(password)
        }
        user = await self._user_repo.create_user(user_data)
        
        return {
            "access_token": create_access_token(user.id),
            "refresh_token": create_refresh_token(user.id),
            "token_type": "bearer"
        }
        
    async def login_user(self, user_data: LoginRequest) -> dict:
        user = await self.user_registration_review(user_data)
        
        if not user:
            raise UserNotFoundError("This user not found.")
        
        password_hashed = getattr(user, "password", None)
        if not password_hashed and not self._hasher.verify(user_data.password, password_hashed):
            raise CredentialError("Wrong password")
        
        return{
            "access_token": create_access_token(user.id),
            "refresh_token": create_refresh_token(user.id),
            "token_type": "bearer"
        }
        
    async def logout_user(self, logout_data: LogoutUser, user_id: UUID) -> dict:
        token = getattr(logout_data, "token", None)
        
        if token is None:
            raise InvalidTokenError("The token does not exist.")
        
        pyload = decode_refresh_token(token)
        jti = pyload.get("jti", token)
        await self._token_repo.create_invalid_token(jti, user_id)
        return{
            "status_code": 200,
            "detail": "successfuly"
        }
        
    async def refresh_token(self, refresh_data: RefreshToken) -> dict:
        token = refresh_data.refresh_token
        
        pyload = decode_refresh_token(token)
        jti = pyload.get("jti", token)
        
        if await self._token_repo.is_invalid(jti):
            raise InvalidTokenError("Token revoked")
        
        user_id = UUID(pyload["sub"])
        user = await self._user_repo.get_user_by_id(user_id)
        
        if not user:
            raise UserNotFoundError()
        
        return {
            "access_token": create_access_token(user.id),
            "refresh_token": create_refresh_token(user.id),
            "token_type": "bearer"
        }
        
    async def delete_accont(self, user_id: UUID) -> dict:
        user = await self._user_repo.delete_user(user_id)
        
        if user is None:
            raise UserNotFoundError("A user with this information does not exist in the system.")
        
        return {
            "status_code": 200,
            "detail": "Deletion completed successfully"
        }