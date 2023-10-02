import enum

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import MetaData, Table, Column, Integer, Identity, String, ForeignKey, Enum, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Role(Base):
    __tablename__ = "Roles"

    class EnumRole(enum.Enum):
        USER = 1
        MODERATOR = 2
        ADMIN = 3

    id = Column("id", Integer, Identity(start=1, increment=1), primary_key=True)
    role = Column("role", Enum(EnumRole), nullable=False)


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "Users"

    id = Column("id", Integer, Identity(start=1, increment=1), primary_key=True)
    name = Column("name", String, nullable=False)
    role_id = Column("role_id", ForeignKey("Roles.id", ondelete="CASCADE"), nullable=False)


class Author(Base):
    __tablename__ = "Authors"

    id = Column("id", Integer, Identity(start=1, increment=1), primary_key=True)
    name = Column("name", String, nullable=False)


class Book(Base):
    __tablename__ = "Books"

    id = Column("id", Integer, Identity(start=1, increment=1), primary_key=True)
    name = Column("name", String, nullable=False)
    year = Column("year", Integer, nullable=False)
    author_id = Column("author_id", ForeignKey("Authors.id", ondelete="CASCADE"), nullable=False)
    annotation = Column("annotation", String, nullable=True)


class Collection(Base):
    __tablename__ = "Collections"

    id = Column("id", Integer, Identity(start=1, increment=1), primary_key=True)
    name = Column("name", String, nullable=False)
    user_id = Column("user_id", ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)


class Review(Base):
    __tablename__ = "Reviews"

    id = Column("id", Integer, Identity(start=1, increment=1), primary_key=True)
    user_id = Column("user_id", ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    book_id = Column("book_id", ForeignKey("Books.id", ondelete="CASCADE"), nullable=False)
    rating = Column("rating", Integer, nullable=False)
    text = Column("text", String, nullable=False)
    created = Column(DateTime(timezone=True), server_default=func.now())


class BookToCollection(Base):
    __tablename__ = "Books Collections"

    id = Column("id", Integer, Identity(start=1, increment=1), primary_key=True)
    collection_id = Column("collection_id", ForeignKey("Collections.id", ondelete="CASCADE"), nullable=False)
    book_id = Column("book_id", ForeignKey("Books.id", ondelete="CASCADE"), nullable=False)


class Genre(Base):
    __tablename__ = "Genres"

    id = Column("id", Integer, Identity(start=1, increment=1), primary_key=True)
    name = Column("name", String, nullable=False)


class GenreToBook(Base):
    __tablename__ = "Books Genres"

    id = Column("id", Integer, Identity(start=1, increment=1), primary_key=True)
    genre_id = Column("genre_id", ForeignKey("Genres.id", ondelete="CASCADE"), nullable=False)
    book_id = Column("book_id", ForeignKey("Books.id", ondelete="CASCADE"), nullable=False)