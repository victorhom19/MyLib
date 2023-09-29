from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.database import get_async_session
from models.models import Book, Author, User, Role, Review, Genre, GenreToBook
from routes.auth_router import current_user


class GenreModel(BaseModel):
    name: str


genres_router = APIRouter()


@genres_router.get("/genres/{genre_id}")
async def get_books_by_genre(genre_id: int,
                             session: AsyncSession = Depends(get_async_session)):
    genre = await session.get(Genre, genre_id)

    statement = select(Book, GenreToBook).where(GenreToBook.genre_id == genre.id)
    books = (await session.execute(statement)).scalars().all()
    
    return {
        "id": genre.id,
        "name": genre.name,
        "books": [
            {
                "id": book.id,
                "name": book.name,
                "year": book.year,
            }
            for book in books
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

        book_dict = {
            "id": book.id,
            "name": book.name,
            "author": {
                "id": author.id,
                "name": author.name
            },
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
        return None
    book = Book(
        name=new_book.name,
        author_id=new_book.author_id,
        year=new_book.year,
        annotation=new_book.annotation
    )
    session.add(book)
    await session.commit()
    return book


@books_router.put("/books/{book_id}")
async def update_book(book_id: int, new_book: BookModel,
                      user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):
    user_role = await session.get(Role, user.role_id)
    if user_role.role != Role.EnumRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    book = await session.get(Book, book_id)
    book.name = new_book.name
    book.author_id = new_book.author_id
    book.year = new_book.year
    book.annotation = new_book.annotation
    await session.commit()
    return book


@books_router.delete("/books/{book_id}")
async def delete_book(book_id: int,
                      user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):
    user_role = await session.get(Role, user.role_id)
    if user_role.role != Role.EnumRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    book = await session.get(Book, book_id)
    await session.delete(book)
    await session.commit()
    return {'removed': book_id}
