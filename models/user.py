from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from tools.initialise_postgres import Base
import uuid


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    
    username: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True,
        index=True
    )
    
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    
    display_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    
    can_upload_videos: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    
    profile_picture_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    
    videos = relationship("Video", back_populates="user", cascade="all, delete")
