from app.models.user import User
from sqlalchemy import  select, delete

from sqlalchemy.ext.asyncio import AsyncSession

from uuid import UUID

class UserRepositories:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def create_user(self, user_data: dict):
        new_user = User(**user_data)
        self.db.add(new_user)
        await self.db.flush()
        await self.db.refresh(new_user)
        return new_user
    
    async def get_user_by_id(self, user_id: UUID):
        user = await self.db.execute(select(User).where(User.id == user_id))
        return user.scalar_one_or_none()
    
    async def get_user_by_phone(self, phone: str):
        user = await self.db.execute(select(User).where(User.phone == phone))
        return user.scalar_one_or_none()
    
    async def get_user_by_email(self, email: str):
        user = await self.db.execute(select(User).where(User.email == email))
        return user.scalar_one_or_none()
    
    async def exists_by_phone(self, phone: str):
        return (await self.get_user_by_phone(phone)) is not None
    
    async def exists_by_email(self, email: str):
        return (await self.get_user_by_email(email)) is not None
    
    async def update_user_data(self, user_id: UUID, user_data: dict):
        user = await self.get_user_by_id(user_id)
        if not user:
            return None
        for key, value in user_data.items:
            setattr(user, key, value)
        await self.db.flush()
        return user
    
    async def delete_user(self, user_id: UUID):
        user = await self.get_user_by_id(user_id)
        if not user:
            return None
        await self.db.delete(user)
        await self.db.flush()
        return user
    