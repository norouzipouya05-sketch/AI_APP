from .config import get_settings

import redis.asyncio as redis

class RedisClient:
    _pool = None
    _settings = get_settings()
    
    @classmethod
    async def get_pool(cls):
        if cls._pool is None:
            cls._pool = redis.ConnectionPool.from_url(
                cls._settings.redis_url,
                decode_responses=True,
                max_connections=cls._settings.redis_max_connection
            )
        return cls._pool
    
    @classmethod
    async def get_redis_connect(cls):
        pool = await cls.get_pool()
        return redis.Redis(connection_pool=pool)
    
async def get_redis() -> redis.Redis:
    return await RedisClient.get_redis_connect()
