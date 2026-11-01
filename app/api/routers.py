from fastapi import APIRouter
from .endpoints.chat import router as agent_router
from .endpoints.auth import router as auth_router
from .endpoints.otp import router as otp_router

router = APIRouter(prefix="/api")

router.include_router(agent_router)
router.include_router(auth_router)
router.include_router(otp_router)
