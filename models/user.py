from backend.db import Base, slug
from sqlalchemy.orm import relationship, Mapped, mapped_column


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str]
    firstname: Mapped[str]
    lastname: Mapped[str]
    age: Mapped[int]
    slug: Mapped[slug]
    tasks = relationship('Task', back_populates='user')

# from sqlalchemy.schema import CreateTable
# print(CreateTable(User.__table__))
