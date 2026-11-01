from datetime import datetime
from uuid6 import uuid7

from app.db.base import Base
from sqlalchemy import String, UUID, func, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

class InvalidToken(Base):
    __tablename__ = "invalid_token"
    
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    jti: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))