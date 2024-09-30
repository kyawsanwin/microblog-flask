from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import ForeignKey, String, Text
from microblog import db
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Blog(db.Model):
    __tablename__ = "blogs"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[Optional[datetime]] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship(back_populates="blogs")  # noqa: F821

    def __repr__(self) -> str:
        return f"{self.id}, {self.title}"

    def get_latest_posts(self, limit):
        return db.session.query(Blog).order_by(Blog.created_at).limit(limit).all()
