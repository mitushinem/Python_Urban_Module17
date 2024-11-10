from typing import Annotated

from sqlalchemy import create_engine, text, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column
from config import settings

# engine = create_engine('sqlite:///taskmanager.db', echo=True)
engine = create_engine(
    url=settings.DATABASE_URL_SQLITE,
    echo=True,
    # pool_size=20,
    # max_overflow=10,
    )

Session = sessionmaker(bind=engine)

str_256 = Annotated[str, 256]
slug = Annotated[str, mapped_column(unique=True, index=True)]

class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"

# with Session() as session:

# with engine.connect() as conn:
#     res = conn.execute(text("select version"))
#     print(res)
# with engine.begin