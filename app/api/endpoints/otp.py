from fastapi import APIRouter, Depends, HTTPException

from app.schemes.request import OTPRequest, OTPVeifyRequest
from app.schemes.response import OTPResponse, OTPResponseVerify
from app.api.dependencies.services import (
    get_otp_service,
    get_redis,
)
from app.services.otp import OTPService
from app.core.exceptions import (
    NoneExistentError,
    OTPExpiredError,
    OTPWrongCode,
)

import pyotp
from redis.asyncio import Redis
from typing import Annotated

router = APIRouter(prefix="/otp", tags=["otp"])

@router.post("/request", response_model=OTPResponse)
async def otp_request(
    otp_data: OTPRequest,
    otp_service: Annotated[OTPService, Depends(get_otp_service)],
    redis: Annotated[Redis, Depends(get_redis)]
):
    try:
        result = await otp_service.otp_request(otp_data, redis)
        return result
    except NoneExistentError as er:
        raise HTTPException(
            status_code=er.status_code, detail=er.default_detail
        )
        
@router.post("/verify", response_model=OTPResponseVerify)
async def verify_token(
    otp_data: OTPVeifyRequest,
    otp_service: Annotated[OTPService, Depends(get_otp_service)],
    redis: Annotated[Redis, Depends(get_redis)]
):
    try:
        result = await otp_service.otp_verify(redis, otp_data)
        return result
    except (OTPWrongCode, OTPExpiredError) as er:
        raise HTTPException(
            status_code=er.status_code, detail=er.default_detail
        )
        
        