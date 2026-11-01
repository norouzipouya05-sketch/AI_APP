from sqlalchemy import String, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class RecoveryCode(Base):
    __tablename__ = "recovery_code"
    
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    recovery_code: Mapped[str] = mapped_column(String(10), nullable=True, primary_key=True)
    
    user: Mapped["User"] = relationship(
        back_populates="recovery_codes",
        uselist=False,
        viewonly=True
    )