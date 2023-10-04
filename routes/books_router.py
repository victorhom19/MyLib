from typing import List, Union

from fastapi import APIRouter, Depends, status, HTTPException, Response
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


class BookSearchModel(BaseModel):
    search_query: Union[None, str]
    genre_ids: Union[None, List[int]]
    year_from: Union[None, int]
    year_to: Union[None, int]
    author_ids: Union[None, List[int]]


books_router = APIRouter()


@books_router.get("/books/{book_id}")
async def get_book(book_id: int,
                   response: Response,
                   session: AsyncSession = Depends(get_async_session)):

    # Check for corresponding book existence
    book = await session.get(Book, book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id={book_id} not found"
        )

    # Select book author
    author = await session.get(Author, book.author_id)

    # Select reviews with corresponding users
    statement = select(Review, User).outerjoin(User, Review.user_id == User.id).where(Review.book_id == book.id)
    reviews_to_users = (await session.execute(statement)).all()
    reviews_count = len(reviews_to_users)
    book_rating = 0
    if reviews_count > 0:
        reviews, users = list(zip(*reviews_to_users))
        book_rating = (sum([review.rating for review in reviews]) / reviews_count) if reviews_count > 0 else 0

    # Select genres
    statement = select(Genre).where(GenreToBook.genre_id == Genre.id, GenreToBook.book_id == book.id)
    genres = (await session.execute(statement)).scalars().all()

    # Format response
    response.status_code = status.HTTP_200_OK
    res = {
        "id": book.id,
        "title": book.title,
        "author": {
            "id": author.id,
            "name": author.name
        },
        "reviews": [
            {
                "id": review.id,
                "user": {
                    "id": user.id,
                    "name": user.name
                },
                "rating": review.rating,
                "text": review.text,
                "created": review.created
            }
            for review, user in reviews_to_users
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

    return res


@books_router.get("/books")
async def get_books(book_search: BookSearchModel,
                    response: Response,
                    session: AsyncSession = Depends(get_async_session)):

    # Select books with corresponding authors initial statement
    statement = select(Book, Author).outerjoin(Author)\
        .where(Book.author_id == Author.id)\


    # Filter books by search phrase
    if book_search.search_query is not None:
        statement = statement.where(Book.title.ilike(f"%{book_search.search_query}%"))

    # Filter books by genres
    if book_search.genre_ids is not None:
        statement = statement.where(GenreToBook.book_id == Book.id, GenreToBook.genre_id.in_(book_search.genre_ids))

    # Filter books by years
    if book_search.year_from is not None:
        statement = statement.where(Book.year >= book_search.year_from)
    if book_search.year_to is not None:
        statement = statement.where(Book.year <= book_search.year_to)

    # Filter books by authors
    if book_search.author_ids is not None:
        statement = statement.where(Book.author_id.in_(book_search.author_ids))

    # Select books with authors
    books_to_authors = (await session.execute(statement)).all()

    res = []
    for book, author in books_to_authors:

        # Select book reviews and collect additional data
        statement = select(Review).where(Review.book_id == book.id)
        reviews = (await session.execute(statement)).scalars().all()
        reviews_count = len(reviews)
        book_rating = (sum([review.rating for review in reviews]) / reviews_count) if reviews_count > 0 else 0

        # Select book genres
        statement = select(Genre).where(GenreToBook.book_id == book.id, Genre.id == GenreToBook.genre_id)
        genres = (await session.execute(statement)).scalars().all()

        # Format response
        formatted_book = {
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
        res.append(formatted_book)

    response.status_code = status.HTTP_200_OK
    return res


@books_router.post("/books")
async def create_book(new_book: BookModel,
                      response: Response,
                      user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):

    # Check for permissions (must be Admin to create book)
    user_role = await session.get(Role, user.role_id)
    if user_role.role != Role.EnumRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to modify data"
        )

    # Check for corresponding author existence
    author = await session.get(Author, new_book.author_id)
    if author is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid request payload. Author with id={new_book.author_id} does not exist"
        )

    # Check for corresponding genres existence
    statement = select(Genre).where(Genre.id.in_(new_book.genre_ids))
    genres = (await session.execute(statement)).scalars().all()
    found_ids = [genre.id for genre in genres]
    missing_genres = [str(genre_id) for genre_id in new_book.genre_ids if genre_id not in found_ids]
    if len(missing_genres) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid request payload. Genres with id={', '.join(missing_genres)} do not exist"
        )

    # Book creation
    book = Book(
        title=new_book.title,
        author_id=new_book.author_id,
        year=new_book.year,
        annotation=new_book.annotation
    )
    session.add(book)
    await session.commit()
    # Creating corresponding books-genres records
    for genre_id in new_book.genre_ids:
        genre_to_book = GenreToBook(
            genre_id=genre_id,
            book_id=book.id
        )
        session.add(genre_to_book)

    # Committing changes
    await session.commit()

    # Format response
    response.status_code = status.HTTP_200_OK
    res = {
        "id": book.id,
        "title": book.title,
        "author": {
            "id": author.id,
            "name": author.name
        },
        "reviews": [],
        "genres": [
            {
                "id": genre.id,
                "name": genre.name
            } for genre in genres
        ],
        "rating": 0,
        "reviews_count": 0,
        "year": book.year,
        "annotation": book.annotation
    }

    return res


@books_router.put("/books/{book_id}")
async def update_book(book_id: int, new_book: BookModel,
                      response: Response,
                      user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):

    # Check for permissions (must be Admin to update book)
    user_role = await session.get(Role, user.role_id)
    if user_role.role != Role.EnumRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to modify data"
        )

    # Check for corresponding book existence
    book = await session.get(Book, book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id={book_id} can not be found"
        )

    # Check for corresponding author existence
    author = await session.get(Author, new_book.author_id)
    if author is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid request payload. Author with id={new_book.author_id} does not exist"
        )

    # Check for corresponding genres existence
    statement = select(Genre).where(Genre.id.in_(new_book.genre_ids))
    genres = (await session.execute(statement)).scalars().all()
    found_ids = [genre.id for genre in genres]
    missing_genres = [str(genre_id) for genre_id in new_book.genre_ids if genre_id not in found_ids]
    if len(missing_genres) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid request payload. Genres with id={', '.join(missing_genres)} do not exist"
        )

    # Updating simple fields
    book.title = new_book.title
    book.year = new_book.year
    book.annotation = new_book.annotation

    # Updating one-to-many relationships (book-authors)
    book.author_id = new_book.author_id

    # Updating many-to-many relationships (books-genres)
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

    # Committing changes
    await session.commit()

    # Collect additional data about book
    statement = select(Review, User).outerjoin(User, Review.user_id == User.id).where(Review.book_id == book.id)
    reviews_to_users = (await session.execute(statement)).all()
    reviews_count = len(reviews_to_users)
    book_rating = 0
    if reviews_count > 0:
        reviews, users = list(zip(*reviews_to_users))
        book_rating = (sum([review.rating for review in reviews]) / reviews_count) if reviews_count > 0 else 0

    # Format response
    response.status_code = status.HTTP_200_OK
    res = {
        "id": book.id,
        "title": book.title,
        "author": {
            "id": author.id,
            "name": author.name
        },
        "reviews": [
            {
                "id": review.id,
                "user": {
                    "id": user.id,
                    "name": user.name
                },
                "rating": review.rating,
                "text": review.text,
                "created": review.created
            }
            for review, user in reviews_to_users
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

    return res


@books_router.delete("/books/{book_id}")
async def delete_book(book_id: int,
                      response: Response,
                      user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):

    # Check for permissions (must be Admin to delete book)
    user_role = await session.get(Role, user.role_id)
    if user_role.role != Role.EnumRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to modify data"
        )

    # Check for corresponding book existence
    book = await session.get(Book, book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id={book_id} does not exist"
        )

    # Committing changes
    await session.delete(book)
    await session.commit()

    # Format response
    response.status_code = status.HTTP_200_OK
    res = {
        "removed": book_id
    }
    return res
