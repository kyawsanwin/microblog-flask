from datetime import datetime, timezone
from typing import Optional
from microblog import db
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, String
from sqlalchemy import Integer


class Todo(db.Model):
    __table__name = "todos"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    is_done: Mapped[Optional[int]] = mapped_column(Integer(), default=0)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[Optional[datetime]] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship(back_populates="todos")  # noqa: F821

    def __repr__(self) -> str:
        return f"Todo({self.id}, {self.title}, {self.is_done})"
