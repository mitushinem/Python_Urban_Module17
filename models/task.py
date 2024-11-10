from datetime import datetime
from typing import Annotated
from backend.db import Base, str_256, slug
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import relationship, Mapped, mapped_column


intpk = Annotated[int, mapped_column(primary_key=True, index=True)]
# created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
created_at = Annotated[datetime, mapped_column(default=datetime.now)]

class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = {'extend_existing': True}
    id: Mapped[intpk]
    title: Mapped[str_256]
    content: Mapped[str]
    priority: Mapped[int] = mapped_column(default=0)
    completed: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    slug: Mapped[slug]
    created_at: Mapped[created_at]
    user = relationship("User", back_populates="tasks")

