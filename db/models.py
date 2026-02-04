from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID


class Base(DeclarativeBase):
    pass


class Video(Base):
    __tablename__ = "videos"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True)
    creator_id: Mapped[str] = mapped_column(UUID(as_uuid=False))
    video_created_at: Mapped[str] = mapped_column(TIMESTAMP)

    views_count: Mapped[int] = mapped_column(Integer)
    likes_count: Mapped[int] = mapped_column(Integer)
    comments_count: Mapped[int] = mapped_column(Integer)
    reports_count: Mapped[int] = mapped_column(Integer)

    created_at: Mapped[str] = mapped_column(TIMESTAMP)
    updated_at: Mapped[str] = mapped_column(TIMESTAMP)


class VideoSnapshot(Base):
    __tablename__ = "video_snapshots"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True)
    video_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("videos.id")
    )

    views_count: Mapped[int] = mapped_column(Integer)
    likes_count: Mapped[int] = mapped_column(Integer)
    comments_count: Mapped[int] = mapped_column(Integer)
    reports_count: Mapped[int] = mapped_column(Integer)

    delta_views_count: Mapped[int] = mapped_column(Integer)
    delta_likes_count: Mapped[int] = mapped_column(Integer)
    delta_comments_count: Mapped[int] = mapped_column(Integer)
    delta_reports_count: Mapped[int] = mapped_column(Integer)

    created_at: Mapped[str] = mapped_column(TIMESTAMP)
    updated_at: Mapped[str] = mapped_column(TIMESTAMP)
