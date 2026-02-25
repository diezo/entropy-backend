from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Float, ForeignKey, String, Text, DateTime, Enum, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from tools.initialise_postgres import Base
import enum
import uuid


class VideoStatus(enum.Enum):
    UPLOADING = "uploading"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


class Video(Base):
    __tablename__ = "videos"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    
    status: Mapped[VideoStatus] = mapped_column(
        Enum(VideoStatus),
        default=VideoStatus.UPLOADING,
        nullable=False
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    
    processing_error: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    
    manifest_s3_key: Mapped[str | None] = mapped_column(
        String(512),
        nullable=True
    )
    
    duration: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )
    
    user = relationship("User", back_populates="videos")
