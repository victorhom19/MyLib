import json
from typing import List, Union

from fastapi import APIRouter, Depends, status, HTTPException, Response
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.database import get_async_session
from cache.cache import get_cache_instance
from models.models import Book, Author, User, Role, Review, Genre, GenreToBook
from routes.auth_router import current_user
from routes.models.books.create_book_model import CreateBookRequestModel, CreateBookResponseModel
from routes.models.books.delete_book_model import DeleteBookModelResponse

from routes.models.books.get_book_model import GetBookResponseModel
from routes.models.books.get_books_model import GetBooksResponseModel, GetBooksRequestModel
from routes.models.books.update_book_model import UpdateBookRequestModel, UpdateBookResponseModel

books_router = APIRouter()


@books_router.get("/{book_id}")
async def get_book(book_id: int,
                   response: Response,
                   session: AsyncSession = Depends(get_async_session)) -> GetBookResponseModel:

    # Check for corresponding book existence
    book = await session.get(Book, book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id={book_id} not found"
        )

    # Check for existing in cache
    cache = get_cache_instance()
    from_cache = cache.get(f'/books/{book_id}')
    if from_cache is not None:
        return GetBookResponseModel.parse_json(from_cache)

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
    res = GetBookResponseModel(
            id=book.id,
            title=book.title,
            author=GetBookResponseModel.AuthorModel(
                id=author.id,
                name=author.name
            ),
            genres=[
                GetBookResponseModel.GenreModel(
                    id=genre.id,
                    name=genre.name
                ) for genre in genres
            ],
            rating=book_rating,
            reviews_count=reviews_count,
            reviews=[
                GetBookResponseModel.ReviewModel(
                    id=review.id,
                    user=GetBookResponseModel.UserModel(
                        id=user.id,
                        name=user.name
                    ),
                    rating=review.rating,
                    text=review.text,
                    created=review.created
                ) for review, user in reviews_to_users
            ],
            year=book.year,
            annotation=book.annotation
        )

    # Cache response
    cache.set(f"/books/{book_id}", json.dumps(res.as_dict()))

    return res


@books_router.get("/")
async def get_books(book_search: GetBooksRequestModel,
                    response: Response,
                    session: AsyncSession = Depends(get_async_session)) -> List[GetBooksResponseModel]:

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
        response.status_code = status.HTTP_200_OK
        book_model = GetBooksResponseModel(
            id=book.id,
            title=book.title,
            author=GetBooksResponseModel.AuthorModel(
                id=author.id,
                name=author.name
            ),
            genres=[
                GetBooksResponseModel.GenreModel(
                    id=genre.id,
                    name=genre.name
                ) for genre in genres
            ],
            rating=book_rating,
            reviews_count=reviews_count,
        )

        res.append(book_model)

    return res


@books_router.post("/")
async def create_book(new_book: CreateBookRequestModel,
                      response: Response,
                      user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)) -> CreateBookResponseModel:

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
    res = CreateBookResponseModel(
            id=book.id,
            title=book.title,
            author=CreateBookResponseModel.AuthorModel(
                id=author.id,
                name=author.name
            ),
            genres=[
                CreateBookResponseModel.GenreModel(
                    id=genre.id,
                    name=genre.name
                ) for genre in genres
            ],
            rating=0,
            reviews_count=0,
            year=book.year,
            annotation=book.annotation
        )

    return res


@books_router.put("/{book_id}")
async def update_book(book_id: int, new_book: UpdateBookRequestModel,
                      response: Response,
                      user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)) -> UpdateBookResponseModel:

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

    # Invalidate cache
    cache = get_cache_instance()
    cache.delete(f'/books/{book_id}')

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
    res = UpdateBookResponseModel(
        id=book.id,
        title=book.title,
        author=UpdateBookResponseModel.AuthorModel(
            id=author.id,
            name=author.name
        ),
        genres=[
            UpdateBookResponseModel.GenreModel(
                id=genre.id,
                name=genre.name
            ) for genre in genres
        ],
        rating=book_rating,
        reviews_count=reviews_count,
        reviews=[
            UpdateBookResponseModel.ReviewModel(
                id=review.id,
                user=UpdateBookResponseModel.UserModel(
                    id=user.id,
                    name=user.name
                ),
                rating=review.rating,
                text=review.text,
                created=review.created
            ) for review, user in reviews_to_users
        ],
        year=book.year,
        annotation=book.annotation
    )

    return res


@books_router.delete("/{book_id}")
async def delete_book(book_id: int,
                      response: Response,
                      user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)) -> DeleteBookModelResponse:

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

    # Get name before delete
    book_title = book.title

    # Committing changes
    await session.delete(book)
    await session.commit()

    # Invalidate cache
    cache = get_cache_instance()
    cache.delete(f'/books/{book_id}')

    # Format response
    response.status_code = status.HTTP_200_OK
    res = DeleteBookModelResponse(
        id=book_id,
        title=book_title
    )
    return res
