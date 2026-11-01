from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager

from app.api.routers import router
from app.middleware.rate_limit import RateLimitMiddleware
from app.core.redis_client import RedisClient

@asynccontextmanager
async def lifespan(app: FastAPI):
    await RedisClient.get_pool()
    
    yield
    
    pool = await RedisClient.get_pool()
    await pool.disconnect
    

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router)
app.add_middleware(RateLimitMiddleware)

if __name__ == "__main__":
    
    uvicorn.run(app, host="127.0.0.1", port=3045)