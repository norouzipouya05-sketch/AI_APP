from redis.asyncio import Redis
import time

LUA_SCRIPT = """

local key = KEYS[1]
local now = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local limit = tonumber(ARGV[3])

redis.call('ZREMRANGEBYSCORE', key, 0, now - window)
local current = redis.call('ZCARD', key)

if current < limit then
    redis.call('ZADD', key, now, now .. ':' .. math.random())
    redis.call('EXPIRE', key, window)
    return { current + 1, limit - (current + 1), now + window}
else
    local oldest = redis.call('ZRANGE', key, 0, 0, 'WITHSCORES')
    local retry_after = (tomunber(oldest[2]) + window) - now
    return {current, 0, retry_after}

"""

class RateLimiter:
    def __init__(self, redis: Redis, key_limiter: str = "rate_limit"):
        self.redis = redis
        self.key = key_limiter
        self._script = None
        
    async def check_request(self, identifier: str, limit: int, window: int) -> dict:
        if self._script is None:
            self._script = self.redis.register_script(LUA_SCRIPT)
            
        key = f"{self.key}:{identifier}"
        now = time.time()
        
        result = await self._script(keys=[key], args=[now, window, limit])
        allowed = int(result[0]) <= limit
        remaining = max(0, int(result[1]))
        
        headers = {
            "RateLimit-Limit": str(limit),
            "RateLimit-Remaining": str(remaining),
            "RateLimit-Reset": str(int(result[2])),
        }
        return allowed, headers
    