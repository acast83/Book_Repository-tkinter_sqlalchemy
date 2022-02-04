from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pathlib import Path


dir_absolute_path = str(Path().absolute())
engine = create_engine("sqlite:///" + dir_absolute_path + "/data.db")


Base = declarative_base()


class Db_Model(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String(25), nullable=False)
    author = Column(String(25), nullable=False)
    year = Column(Integer, nullable=True)
    isbn = Column(Integer, nullable=False)


def create_database():
    Base.metadata.create_all(engine)


# create_database()
