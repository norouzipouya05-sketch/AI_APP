from datetime import datetime
from typing import Optional, List
from uuid6 import uuid7

from sqlalchemy import String, ForeignKey, UUID, DateTime, func, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class User(Base):
    __tablename__ = "User"
    
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    phone: Mapped[str] = mapped_column(String(15), unique=True, nullable=False)
    create_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    password_hash: Mapped[str] = mapped_column(Text, nullable=True)
    
    recovery_codes: Mapped[Optional[list["RecoveryCode"]]] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )