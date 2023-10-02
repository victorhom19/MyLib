from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.database import get_async_session
from models.models import Book, Author, User, Role, Review, Genre, GenreToBook
from routes.auth_router import current_user


class BookModel(BaseModel):
    title: str
    author_id: int
    year: int
    annotation: str
    genre_ids: List[int]


books_router = APIRouter()


@books_router.get("/books/{book_id}")
async def get_book(book_id: int,
                   session: AsyncSession = Depends(get_async_session)):
    book = await session.get(Book, book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id={book_id} can not be found"
        )

    author = await session.get(Author, book.author_id)
    statement = select(Review).where(Review.book_id == book.id)
    reviews = (await session.execute(statement)).scalars().all()
    reviews_count = len(reviews)
    book_rating = (sum([review.rating for review in reviews]) / reviews_count) if reviews_count > 0 else 0

    statement = select(Genre).where(GenreToBook.book_id == book.id)
    genres = (await session.execute(statement)).scalars().all()

    return {
        "id": book.id,
        "title": book.title,
        "author": {
            "id": author.id,
            "name": author.name
        },
        "reviews": [
            {
                "id": review.id,
                "rating": review.rating,
                "text": review.text,
                "created": review.created
            }
            for review in reviews
        ],
        "genres": [
            {
                "id": genre.id,
                "name": genre.name
            } for genre in genres
        ],
        "rating": book_rating,
        "reviews_count": reviews_count,
        "year": book.year,
        "annotation": book.annotation
    }


@books_router.get("/books")
async def get_books(session: AsyncSession = Depends(get_async_session)):
    statement = select(Book, Author).outerjoin(Author).where(Book.author_id == Author.id)
    data = (await session.execute(statement)).all()

    books_list = []
    for book, author in data:
        statement = select(Review).where(Review.book_id == book.id)
        reviews = (await session.execute(statement)).scalars().all()
        reviews_count = len(reviews)
        book_rating = (sum([review.rating for review in reviews]) / reviews_count) if reviews_count > 0 else 0

        statement = select(Genre).where(GenreToBook.book_id == book.id)
        genres = (await session.execute(statement)).scalars().all()

        book_dict = {
            "id": book.id,
            "title": book.title,
            "author": {
                "id": author.id,
                "name": author.name
            },
            "genres": [
                {
                    "id": genre.id,
                    "name": genre.name
                } for genre in genres
            ],
            "rating": book_rating,
            "reviews_count": reviews_count,
            "year": book.year,
            "annotation": book.annotation
        }
        books_list.append(book_dict)

    return books_list


@books_router.post("/books")
async def create_book(new_book: BookModel,
                      user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):

    user_role = await session.get(Role, user.role_id)
    if user_role.role != Role.EnumRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to modify data"
        )

    author = await session.get(Author, new_book.author_id)
    if author is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid request payload. Author with id={new_book.author_id} does not exist"
        )

    statement = select(Genre).where(Genre.id.in_(new_book.genre_ids))
    genres = (await session.execute(statement)).scalars().all()
    found_ids = [genre.id for genre in genres]
    missing_genres = [str(genre_id) for genre_id in new_book.genre_ids if genre_id not in found_ids]
    if len(missing_genres) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid request payload. Genres with id={', '.join(missing_genres)} do not exist"
        )

    book = Book(
        name=new_book.name,
        author_id=new_book.author_id,
        year=new_book.year,
        annotation=new_book.annotation
    )
    session.add(book)
    await session.commit()
    for genre_id in new_book.genre_ids:
        genre_to_book = GenreToBook(
            genre_id=genre_id,
            book_id=book.id
        )
        session.add(genre_to_book)
    await session.commit()
    return book


@books_router.put("/books/{book_id}")
async def update_book(book_id: int, new_book: BookModel,
                      user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):

    user_role = await session.get(Role, user.role_id)
    if user_role.role != Role.EnumRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to modify data"
        )

    book = await session.get(Book, book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id={book_id} can not be found"
        )

    book.name = new_book.name
    book.author_id = new_book.author_id
    book.year = new_book.year
    book.annotation = new_book.annotation
    await session.commit()

    statement = select(GenreToBook).where(GenreToBook.book_id == book.id)
    genres_to_book = (await session.execute(statement)).scalars().all()
    for genre_to_book in genres_to_book:
        await session.delete(genre_to_book)
    for genre_id in new_book.genre_ids:
        genre_to_book = GenreToBook(
            genre_id=genre_id,
            book_id=book.id
        )
        session.add(genre_to_book)
    await session.commit()
    return book


@books_router.delete("/books/{book_id}")
async def delete_book(book_id: int,
                      user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):
    user_role = await session.get(Role, user.role_id)
    if user_role.role != Role.EnumRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to modify data"
        )

    book = await session.get(Book, book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id={book_id} does not exist"
        )

    await session.delete(book)
    await session.commit()
    return {'removed': book_id}
