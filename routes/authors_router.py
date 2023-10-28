import json
from typing import List

from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.database import get_async_session
from cache.cache import get_cache_instance
from models.models import Book, Author, User, Role, Review, Genre, GenreToBook
from routes.auth_router import current_user
from routes.models.authors.create_author_model import CreateAuthorRequestModel, CreateAuthorResponseModel
from routes.models.authors.delete_author_model import DeleteAuthorResponseModel
from routes.models.authors.get_author_model import GetAuthorResponseModel
from routes.models.authors.get_authors_model import GetAuthorsResponseModel
from routes.models.authors.update_author_model import UpdateAuthorRequestModel, UpdateAuthorResponseModel

authors_router = APIRouter()


@authors_router.get("/{author_id}")
async def get_author(author_id: int,
                     response: Response,
                     session: AsyncSession = Depends(get_async_session)) -> GetAuthorResponseModel:

    # Check for existing in cache
    cache = get_cache_instance()
    from_cache = cache.get(f'/authors/{author_id}')
    if from_cache is not None:
        return GetAuthorResponseModel.parse_json(from_cache)

    # Check for corresponding author existence
    author = await session.get(Author, author_id)
    if author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id={author_id} not found"
        )

    statement = select(Book).where(Book.author_id == author.id)
    books = (await session.execute(statement)).scalars().all()
    books_list = []
    for book in books:
        # Select book reviews and collect additional data
        statement = select(Review).where(Review.book_id == book.id)
        reviews = (await session.execute(statement)).scalars().all()
        reviews_count = len(reviews)
        book_rating = (sum([review.rating for review in reviews]) / reviews_count) if reviews_count > 0 else 0

        # Select book genres
        statement = select(Genre).where(GenreToBook.book_id == book.id, Genre.id == GenreToBook.genre_id)
        genres = (await session.execute(statement)).scalars().all()

        book_model = GetAuthorResponseModel.BookModel(
            id=book.id,
            title=book.title,
            genres=[
                GetAuthorResponseModel.GenreModel(
                    id=genre.id,
                    name=genre.name
                ) for genre in genres
            ],
            rating=book_rating,
            reviews_count=reviews_count,
        )
        books_list.append(book_model)

    # Format response
    response.status_code = status.HTTP_200_OK
    res = GetAuthorResponseModel(
        id=author.id,
        name=author.name,
        about=author.about,
        books=books_list
    )

    # Cache response
    cache.set(f"/authors/{author.id}", json.dumps(res.as_dict()))

    return res


@authors_router.get("/")
async def get_authors(response: Response,
                      session: AsyncSession = Depends(get_async_session)) -> List[GetAuthorsResponseModel]:

    statement = select(Author)
    authors = (await session.execute(statement)).scalars().all()
    res = []
    for author in authors:

        statement = select(Book).where(Book.author_id == author.id)
        books = (await session.execute(statement)).scalars().all()
        books_list = []
        for book in books:
            # Select book reviews and collect additional data
            statement = select(Review).where(Review.book_id == book.id)
            reviews = (await session.execute(statement)).scalars().all()
            reviews_count = len(reviews)
            book_rating = (sum([review.rating for review in reviews]) / reviews_count) if reviews_count > 0 else 0

            # Select book genres
            statement = select(Genre).where(GenreToBook.book_id == book.id, Genre.id == GenreToBook.genre_id)
            genres = (await session.execute(statement)).scalars().all()

            book_model = GetAuthorsResponseModel.BookModel(
                id=book.id,
                title=book.title,
                genres=[
                    GetAuthorsResponseModel.GenreModel(
                        id=genre.id,
                        name=genre.name
                    ) for genre in genres
                ],
                rating=book_rating,
                reviews_count=reviews_count,
            )
            books_list.append(book_model)

        author_model = GetAuthorsResponseModel(
            id=author.id,
            name=author.name,
            about=author.about,
            books=books_list
        )

        res.append(author_model)

    # Format response
    response.status_code = status.HTTP_200_OK

    return res


@authors_router.post("/")
async def create_author(new_author: CreateAuthorRequestModel,
                        response: Response,
                        user: User = Depends(current_user),
                        session: AsyncSession = Depends(get_async_session)) -> CreateAuthorResponseModel:

    # Check for permissions (must be Admin to create author)
    user_role = await session.get(Role, user.role_id)
    if user_role.role != Role.EnumRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to modify data"
        )

    # Author creation
    author = Author(
        name=new_author.name,
        about=new_author.about
    )

    session.add(author)

    # Committing changes
    await session.commit()

    # Format response
    response.status_code = status.HTTP_200_OK
    res = CreateAuthorResponseModel(
        id=author.id,
        name=author.name,
        about=author.about,
        books=[]
    )

    return res


@authors_router.put("/{author_id}")
async def update_author(author_id: int, new_author: UpdateAuthorRequestModel,
                        response: Response,
                        user: User = Depends(current_user),
                        session: AsyncSession = Depends(get_async_session)) -> UpdateAuthorResponseModel:

    # Check for permissions (must be Admin to update author)
    user_role = await session.get(Role, user.role_id)
    if user_role.role != Role.EnumRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to modify data"
        )

    # Check for corresponding author existence
    author = await session.get(Author, author_id)
    if author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id={author_id} can not be found"
        )

    # Updating simple fields
    author.name = new_author.name
    author.about = new_author.about

    # Committing changes
    await session.commit()

    # Invalidate cache
    cache = get_cache_instance()
    cache.delete(f'/authors/{author.id}')

    # Collect additional data about author
    statement = select(Book).where(Book.author_id == author.id)
    books = (await session.execute(statement)).scalars().all()
    books_list = []
    for book in books:
        # Select book reviews and collect additional data
        statement = select(Review).where(Review.book_id == book.id)
        reviews = (await session.execute(statement)).scalars().all()
        reviews_count = len(reviews)
        book_rating = (sum([review.rating for review in reviews]) / reviews_count) if reviews_count > 0 else 0

        # Select book genres
        statement = select(Genre).where(GenreToBook.book_id == book.id, Genre.id == GenreToBook.genre_id)
        genres = (await session.execute(statement)).scalars().all()

        book_model = UpdateAuthorResponseModel.BookModel(
            id=book.id,
            title=book.title,
            genres=[
                UpdateAuthorResponseModel.GenreModel(
                    id=genre.id,
                    name=genre.name
                ) for genre in genres
            ],
            rating=book_rating,
            reviews_count=reviews_count,
        )
        books_list.append(book_model)

    # Format response
    response.status_code = status.HTTP_200_OK
    res = UpdateAuthorResponseModel(
        id=author.id,
        name=author.name,
        about=author.about,
        books=books_list
    )
    return res


@authors_router.delete("/{author_id}")
async def delete_author(author_id: int,
                        response: Response,
                        user: User = Depends(current_user),
                        session: AsyncSession = Depends(get_async_session)) -> DeleteAuthorResponseModel:

    # Check for permissions (must be Admin to delete author)
    user_role = await session.get(Role, user.role_id)
    if user_role.role != Role.EnumRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to modify data"
        )

    # Check for corresponding author existence
    author = await session.get(Author, author_id)
    if author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id={author_id} can not be found"
        )

    # Get name before delete
    author_name = author.name

    # Committing changes
    await session.delete(author)
    await session.commit()

    # Invalidate cache
    cache = get_cache_instance()
    cache.delete(f'/authors/{author.id}')

    # Format response
    response.status_code = status.HTTP_200_OK
    res = DeleteAuthorResponseModel(
        id=author_id,
        name=author_name
    )
    return res

