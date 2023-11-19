import asyncio

from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import DB_USER, DB_PASS, DB_HOST, DB_HOST_PORT, DB_NAME
from models import Role, Author, Book, Genre, GenreToBook, User, Collection, BookToCollection, Review

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
        await session.execute(text('TRUNCATE TABLE "Books Collections" RESTART IDENTITY CASCADE'))
        await session.execute(text('TRUNCATE TABLE "Books Genres" RESTART IDENTITY CASCADE'))
        await session.execute(text('TRUNCATE TABLE "Collections" RESTART IDENTITY CASCADE'))
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
            Author(name='Дэн Браун', about=""),
            Author(name='Энди Вейер', about=""),
            Author(name='Стивен Кинг', about=""),
            Author(name='Джейн Остин', about=""),
            Author(name='Рэй Брэдбери', about=""),
            Author(name='Клайв Льюис', about=""),
            Author(name='Льюис Кэрролл', about="")
        ]
        session.add_all(authors)
        await session.commit()


async def fill_books():
    async with async_session_maker() as session:
        with open('annotations/origin.txt', encoding="utf-8") as f:
            origin_annotation = '\n'.join(f.readlines())
        with open('annotations/angels_and_demons.txt', encoding="utf-8") as f:
            angels_and_demons_annotation = '\n'.join(f.readlines())
        with open('annotations/digital_fortress.txt', encoding="utf-8") as f:
            digital_fortress_annotation = '\n'.join(f.readlines())
        with open('annotations/artemis.txt', encoding="utf-8") as f:
            artemis_annotation = '\n'.join(f.readlines())
        with open('annotations/martian.txt', encoding="utf-8") as f:
            martian_annotation = '\n'.join(f.readlines())
        with open('annotations/project_hail_mary.txt', encoding="utf-8") as f:
            project_hail_mary_annotation = '\n'.join(f.readlines())
        with open('annotations/the_shining.txt', encoding="utf-8") as f:
            the_shining_annotation = '\n'.join(f.readlines())
        with open('annotations/it.txt', encoding="utf-8") as f:
            it_annotation = '\n'.join(f.readlines())
        with open('annotations/dark_tower.txt', encoding="utf-8") as f:
            dark_tower_annotation = '\n'.join(f.readlines())
        with open('annotations/pride_and_prejudice.txt', encoding="utf-8") as f:
            pride_and_prejudice_annotation = '\n'.join(f.readlines())
        with open('annotations/farenheit_451.txt', encoding="utf-8") as f:
            farenheit_451_annotation = '\n'.join(f.readlines())
        with open('annotations/the_lion_the_witch_and_the_wardrobe.txt', encoding="utf-8") as f:
            the_lion_the_witch_and_the_wardrobe_annotation = '\n'.join(f.readlines())
        with open('annotations/alices_adventures_in_wonderland.txt', encoding="utf-8") as f:
            alices_adventures_in_wonderland_annotation = '\n'.join(f.readlines())

        books = [
            Book(title='Происхождение', year=2017, author_id=1, annotation=origin_annotation),
            Book(title='Ангелы и демоны', year=2000, author_id=1, annotation=angels_and_demons_annotation),
            Book(title='Цифровая крепость', year=1998, author_id=1, annotation=digital_fortress_annotation),

            Book(title='Артемида', year=2017, author_id=2, annotation=artemis_annotation),
            Book(title='Марсианин', year=2011, author_id=2, annotation=martian_annotation),
            Book(title='Проект "Аве Мария"', year=2021, author_id=2, annotation=project_hail_mary_annotation),

            Book(title='Сияние', year=1977, author_id=3, annotation=the_shining_annotation),
            Book(title='Оно', year=1986, author_id=3, annotation=it_annotation),
            Book(title='Темая башня: Стрелок', year=1982, author_id=3, annotation=dark_tower_annotation),

            Book(title='Гордость и предубеждение', year=1813, author_id=4, annotation=pride_and_prejudice_annotation),

            Book(title='451 градус по Фаренгейту', year=1953, author_id=5, annotation=farenheit_451_annotation),

            # Book(title='Лев, колдунья и платяной шкаф', year=1950, author_id=6, annotation=the_lion_the_witch_and_the_wardrobe_annotation),

            Book(title='Алиса в Стране чудес', year=1865, author_id=7, annotation=alices_adventures_in_wonderland_annotation)
        ]

        session.add_all(books)
        await session.commit()


async def fill_genres():
    async with async_session_maker() as session:
        genres = [
            Genre(name='Детектив'),
            Genre(name='Триллер'),
            Genre(name='Научная фантастика'),
            Genre(name='Мистика'),
            Genre(name='Ужасы'),
            Genre(name='Фэнтези'),
            Genre(name='Любовный роман'),
            Genre(name='Сказки')
        ]
        session.add_all(genres)
        await session.commit()


async def fill_book_genres():
    async with async_session_maker() as session:
        book_genres = [
            GenreToBook(book_id=1, genre_id=1),
            GenreToBook(book_id=1, genre_id=2),

            GenreToBook(book_id=2, genre_id=1),
            GenreToBook(book_id=2, genre_id=2),

            GenreToBook(book_id=3, genre_id=1),
            GenreToBook(book_id=3, genre_id=2),


            GenreToBook(book_id=4, genre_id=3),
            GenreToBook(book_id=5, genre_id=3),
            GenreToBook(book_id=6, genre_id=3),

            GenreToBook(book_id=7, genre_id=4),
            GenreToBook(book_id=7, genre_id=5),

            GenreToBook(book_id=8, genre_id=4),
            GenreToBook(book_id=8, genre_id=5),

            GenreToBook(book_id=9, genre_id=6),

            GenreToBook(book_id=10, genre_id=7),

            GenreToBook(book_id=11, genre_id=3),

            GenreToBook(book_id=12, genre_id=8),
        ]
        session.add_all(book_genres)
        await session.commit()


async def fill_collections():
    async with async_session_maker() as session:
        collections = [
            Collection(title="Буду читать", user_id=1),
            Collection(title="Читаю", user_id=1),
            Collection(title="Прочитано", user_id=1),
            Collection(title="Буду читать", user_id=2),
            Collection(title="Читаю", user_id=2),
            Collection(title="Прочитано", user_id=2),
            Collection(title="Буду читать", user_id=3),
            Collection(title="Читаю", user_id=3),
            Collection(title="Прочитано", user_id=3),
            Collection(title="Буду читать", user_id=4),
            Collection(title="Читаю", user_id=4),
            Collection(title="Прочитано", user_id=4),
            Collection(title="Буду читать", user_id=5),
            Collection(title="Читаю", user_id=5),
            Collection(title="Прочитано", user_id=5),
            Collection(title="Коллекция Сергея", user_id=1),
            Collection(title="Коллекция Виктора", user_id=2),
            Collection(title="Коллекция Павла", user_id=3),
            Collection(title="Коллекция модератора", user_id=4),
            Collection(title="Коллекция администратора", user_id=5),
        ]
        session.add_all(collections)
        await session.commit()


async def fill_book_to_collections():
    async with async_session_maker() as session:
        book_to_collections = [
            BookToCollection(book_id=1, collection_id=16),
            BookToCollection(book_id=2, collection_id=16),
            BookToCollection(book_id=3, collection_id=17),
            BookToCollection(book_id=4, collection_id=17),
            BookToCollection(book_id=5, collection_id=18),
            BookToCollection(book_id=6, collection_id=18),
            BookToCollection(book_id=7, collection_id=19),
            BookToCollection(book_id=8, collection_id=19),
            BookToCollection(book_id=9, collection_id=20),
            BookToCollection(book_id=10, collection_id=20),
        ]
        session.add_all(book_to_collections)
        await session.commit()


async def fill_reviews():
    with open('reviews/review_1.txt', encoding="utf-8") as f:
        review_1 = '\n'.join(f.readlines())
    with open('reviews/review_2.txt', encoding="utf-8") as f:
        review_2 = '\n'.join(f.readlines())
    with open('reviews/review_3.txt', encoding="utf-8") as f:
        review_3 = '\n'.join(f.readlines())
    with open('reviews/review_4.txt', encoding="utf-8") as f:
        review_4 = '\n'.join(f.readlines())
    with open('reviews/review_5.txt', encoding="utf-8") as f:
        review_5 = '\n'.join(f.readlines())
    with open('reviews/review_6.txt', encoding="utf-8") as f:
        review_6 = '\n'.join(f.readlines())
    with open('reviews/review_7.txt', encoding="utf-8") as f:
        review_7 = '\n'.join(f.readlines())
    with open('reviews/review_8.txt', encoding="utf-8") as f:
        review_8 = '\n'.join(f.readlines())
    with open('reviews/review_9.txt', encoding="utf-8") as f:
        review_9 = '\n'.join(f.readlines())
    with open('reviews/review_10.txt', encoding="utf-8") as f:
        review_10 = '\n'.join(f.readlines())
    with open('reviews/review_11.txt', encoding="utf-8") as f:
        review_11 = '\n'.join(f.readlines())
    with open('reviews/review_12.txt', encoding="utf-8") as f:
        review_12 = '\n'.join(f.readlines())
    with open('reviews/review_13.txt', encoding="utf-8") as f:
        review_13 = '\n'.join(f.readlines())
    with open('reviews/review_14.txt', encoding="utf-8") as f:
        review_14 = '\n'.join(f.readlines())
    with open('reviews/review_15.txt', encoding="utf-8") as f:
        review_15 = '\n'.join(f.readlines())
    with open('reviews/review_16.txt', encoding="utf-8") as f:
        review_16 = '\n'.join(f.readlines())
    with open('reviews/review_17.txt', encoding="utf-8") as f:
        review_17 = '\n'.join(f.readlines())
    with open('reviews/review_18.txt', encoding="utf-8") as f:
        review_18 = '\n'.join(f.readlines())
    with open('reviews/review_19.txt', encoding="utf-8") as f:
        review_19 = '\n'.join(f.readlines())
    with open('reviews/review_20.txt', encoding="utf-8") as f:
        review_20 = '\n'.join(f.readlines())
    with open('reviews/review_21.txt', encoding="utf-8") as f:
        review_21 = '\n'.join(f.readlines())
    with open('reviews/review_22.txt', encoding="utf-8") as f:
        review_22 = '\n'.join(f.readlines())
    with open('reviews/review_23.txt', encoding="utf-8") as f:
        review_23 = '\n'.join(f.readlines())


    async with async_session_maker() as session:
        reviews = [
            Review(user_id=1, book_id=1, rating=5, text=review_1),
            Review(user_id=2, book_id=1, rating=5, text=review_2),

            Review(user_id=2, book_id=2, rating=5, text=review_3),
            Review(user_id=3, book_id=2, rating=4, text=review_4),

            Review(user_id=3, book_id=3, rating=5, text=review_5),
            Review(user_id=4, book_id=3, rating=4, text=review_6),

            Review(user_id=4, book_id=4, rating=3, text=review_7),
            Review(user_id=5, book_id=4, rating=1, text=review_8),

            Review(user_id=4, book_id=5, rating=5, text=review_9),
            Review(user_id=5, book_id=5, rating=5, text=review_10),

            Review(user_id=5, book_id=6, rating=5, text=review_11),
            Review(user_id=1, book_id=6, rating=5, text=review_12),

            Review(user_id=1, book_id=7, rating=2, text=review_13),
            Review(user_id=2, book_id=7, rating=3, text=review_14),

            Review(user_id=2, book_id=8, rating=5, text=review_15),
            Review(user_id=3, book_id=8, rating=5, text=review_16),

            Review(user_id=3, book_id=9, rating=4, text=review_17),
            Review(user_id=4, book_id=9, rating=5, text=review_18),

            Review(user_id=4, book_id=10, rating=1, text=review_19),
            Review(user_id=5, book_id=10, rating=5, text=review_20),

            Review(user_id=5, book_id=11, rating=5, text=review_21),
            Review(user_id=1, book_id=11, rating=5, text=review_22),

            Review(user_id=1, book_id=12, rating=4, text=review_23),
        ]
        session.add_all(reviews)
        await session.commit()


async def generate(force=False, users_created=False):
    await clear(force=force)
    if force:
        await fill_roles()
    await fill_authors()
    await fill_books()
    await fill_genres()
    await fill_book_genres()
    if users_created:
        await fill_collections()
        await fill_book_to_collections()
        await fill_reviews()

if __name__ == '__main__':
    asyncio.run(generate(force=False, users_created=True))

