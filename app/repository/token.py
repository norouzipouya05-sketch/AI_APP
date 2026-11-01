from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.invalid_token import InvalidToken

class TokenRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def create_invalid_token(self, jti: str, user_id: UUID):
        invalid_token = InvalidToken(jti=jti, user_id=user_id)
        self.db.add(invalid_token)
        await self.db.flush()
        return invalid_token
    
    async def is_invalid(self, jti: str):
        result = await self.db.execute(select(InvalidToken).where(InvalidToken.jti == jti))
        return result.scalar_one_or_none() is not None        