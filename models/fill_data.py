import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import DB_USER, DB_PASS, DB_HOST, DB_HOST_PORT, DB_NAME
from models import Role, Author, Book, Genre, GenreToBook

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_HOST_PORT}/{DB_NAME}"


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def clear(force=False):
    async with async_session_maker() as session:
        if force:
            await session.execute(text('TRUNCATE TABLE "Users" RESTART IDENTITY CASCADE'))
            await session.execute(text('TRUNCATE TABLE "Roles" RESTART IDENTITY CASCADE'))
        await session.execute(text('TRUNCATE TABLE "Authors" RESTART IDENTITY CASCADE'))
        await session.execute(text('TRUNCATE TABLE "Books" RESTART IDENTITY CASCADE'))
        await session.execute(text('TRUNCATE TABLE "Books Compilations" RESTART IDENTITY CASCADE'))
        await session.execute(text('TRUNCATE TABLE "Books Genres" RESTART IDENTITY CASCADE'))
        await session.execute(text('TRUNCATE TABLE "Books Genres" RESTART IDENTITY CASCADE'))
        await session.execute(text('TRUNCATE TABLE "Genres" RESTART IDENTITY CASCADE'))
        await session.execute(text('TRUNCATE TABLE "Reviews" RESTART IDENTITY CASCADE'))
        await session.commit()


async def fill_roles():
    async with async_session_maker() as session:
        user_role = Role(role=Role.EnumRole.USER)
        moderator_role = Role(role=Role.EnumRole.MODERATOR)
        admin_role = Role(role=Role.EnumRole.ADMIN)
        session.add_all([user_role, moderator_role, admin_role])
        await session.commit()


async def fill_authors():
    async with async_session_maker() as session:
        authors = [
            Author(name='Author 1'),
            Author(name='Author 2'),
            Author(name='Author 3')
        ]
        session.add_all(authors)
        await session.commit()


async def fill_books():
    async with async_session_maker() as session:
        books = [
            Book(name='Book 1', year=2001, author_id=1, annotation='Annotation 1'),
            Book(name='Book 2', year=2002, author_id=1, annotation='Annotation 2'),
            Book(name='Book 3', year=2003, author_id=1, annotation='Annotation 3'),

            Book(name='Book 4', year=2002, author_id=2, annotation='Annotation 4'),
            Book(name='Book 5', year=2003, author_id=2, annotation='Annotation 5'),
            Book(name='Book 6', year=2004, author_id=2, annotation='Annotation 6'),

            Book(name='Book 7', year=2003, author_id=3, annotation='Annotation 7'),
            Book(name='Book 8', year=2004, author_id=3, annotation='Annotation 8'),
            Book(name='Book 9', year=2005, author_id=3, annotation='Annotation 9')
        ]

        session.add_all(books)
        await session.commit()


async def fill_genres():
    async with async_session_maker() as session:
        genres = [
            Genre(name='action'),
            Genre(name='adventure'),
            Genre(name='comedy'),
            Genre(name='drama'),
            Genre(name='science fiction'),
            Genre(name='romance'),
            Genre(name='thriller'),
            Genre(name='horror')
        ]
        session.add_all(genres)
        await session.commit()


async def fill_book_genres():
    async with async_session_maker() as session:
        book_genres = [
            GenreToBook(book_id=1, genre_id=1),
            GenreToBook(book_id=1, genre_id=2),

            GenreToBook(book_id=2, genre_id=2),
            GenreToBook(book_id=2, genre_id=3),

            GenreToBook(book_id=3, genre_id=3),
            GenreToBook(book_id=3, genre_id=4),

            GenreToBook(book_id=4, genre_id=4),
            GenreToBook(book_id=4, genre_id=5),

            GenreToBook(book_id=5, genre_id=5),
            GenreToBook(book_id=5, genre_id=6),

            GenreToBook(book_id=6, genre_id=6),
            GenreToBook(book_id=6, genre_id=7),

            GenreToBook(book_id=7, genre_id=7),
            GenreToBook(book_id=7, genre_id=8),

            GenreToBook(book_id=8, genre_id=1),
            GenreToBook(book_id=8, genre_id=3),

            GenreToBook(book_id=9, genre_id=2),
            GenreToBook(book_id=9, genre_id=4),
        ]
        session.add_all(book_genres)
        await session.commit()



async def generate():
    await clear(force=False)
    # await fill_roles()
    await fill_authors()
    await fill_books()
    await fill_genres()
    await fill_book_genres()


if __name__ == '__main__':
    asyncio.run(generate())
