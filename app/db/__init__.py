from .deps import get_db
from .base import Base
from .session import engine


async def create_table() -> None:
    
    from app import models

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
__all__ = ["get_db", "engine", "Base", "create_table"]