from app.services.email import EmailServise
from app.services.phone import PhoneService
from app.repository.user import UserRepositories
from app.core.config import get_settings
from app.schemes.request import OTPRequest, OTPVeifyRequest
from app.core.exceptions import (
    NoneExistentError,
    OTPExpiredError,
    OTPWrongCode,
)

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
import pyotp

settings = get_settings()

class OTPService:
    def __init__(self, db: AsyncSession):
        self.secret = pyotp.random_base32()
        self._email_service = EmailServise
        self._phone_service = PhoneService
        self._user_repo = UserRepositories(db)
        
    async def otp_request(self, redis: Redis, otp_data:OTPRequest) -> dict:
        phone = otp_data.phone
        email = otp_data.email
        
        identifier = (phone if phone else email)
        
        if not identifier:
            raise NoneExistentError("Email or mobile number not entered")
        
        cooldown_key = f"otp_cooldownt:{identifier}"
        ttl = await redis.ttl(cooldown_key)
        if ttl > 0 :
            return {
                "detail": "successfuly",
                "status_code": 200,
                "code": await redis.get(f"otp_code:{identifier}")
            }
            
        totp = pyotp.TOTP(self.secret, interval=settings.otp_ttl_sec, digits=4)
        code = totp.now()
        
        await redis.setex(f"otp_code:{identifier}", settings.otp_ttl_sec, code)
        await redis.setex(f"otp_secret:{identifier}", settings.otp_ttl_sec, self.secret)
        await redis.setex(cooldown_key, settings.otp_request_cooldown_sec, 1)
        
        response = None
        
        if phone:
            await self._phone_service.send_otp_phone(phone, code)
            
        if email:
            await self._email_service.send_otp_email(email, code, settings.otp_ttl_sec)
            
        return {
            "detail": "success",
            "status_code": 200,
            "message": str(response),
            "identifier": identifier,
            "ttl": settings.otp_ttl_sec,
            "code": code
        }
        
    async def otp_verify(self, redis: Redis, otp_data: OTPVeifyRequest) -> dict:
        
        identifier = otp_data.phone
        
        if not identifier:
            raise NoneExistentError("mobile number not intered")
        
        secret = await redis.get(f"otp_secret:{identifier}")
        
        if not secret:
            raise OTPExpiredError()
        
        if isinstance(secret, bytes):
            secret = secret.decode()
            
        totp = pyotp.TOTP(secret, interval=settings.otp_ttl_sec, digits=4)
        
        if not totp.verify(str(otp_data.code), valid_window=1):
            raise OTPWrongCode()
        
        await redis.delete(f"otp_secret:{identifier}")
        await redis.delete(f"otp_code:{identifier}")
        
        challenge_token = pyotp.TOTP(secret, interval=settings.otp_ttl_sec, digits=6)
        await redis.setex(f"challenge_secret:{identifier}", settings.otp_ttl_sec, secret)
        
        return {
            "detail": "success",
            "status_code": 200,
            "challenge_token": str(challenge_token.now()),
            "ttl": await redis.ttl(f"challenge_token:{identifier}")
        }