import json
from typing import List

from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.database import get_async_session
from cache.cache import get_cache_instance
from models.models import Book, Author, User, Role, Review, Genre, GenreToBook
from routes.auth_router import current_user
from routes.models.genres.create_genre_model import CreateGenreResponseModel, CreateGenreRequestModel
from routes.models.genres.delete_genre_model import DeleteGenreResponseModel
from routes.models.genres.get_genre_model import GetGenreResponseModel
from routes.models.genres.get_genres_model import GetGenresResponseModel
from routes.models.genres.update_genre_model import UpdateGenreRequestModel, UpdateGenreResponseModel

genres_router = APIRouter()


@genres_router.get("/{genre_id}")
async def get_genre(genre_id: int,
                    response: Response,
                    session: AsyncSession = Depends(get_async_session)) -> GetGenreResponseModel:

    # Check for existing in cache
    cache = get_cache_instance()
    from_cache = cache.get(f'/genres/{genre_id}')
    if from_cache is not None:
        return GetGenreResponseModel.parse_json(from_cache)

    genre = await session.get(Genre, genre_id)
    if genre is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Genre with id={genre_id} not found"
        )

    # Format response
    response.status_code = status.HTTP_200_OK
    res = GetGenreResponseModel(
        id=genre.id,
        name=genre.name
    )

    # Cache response
    cache.set(f"/genres/{genre.id}", json.dumps(res.as_dict()))

    return res


@genres_router.get("/")
async def get_genres(response: Response,
                     session: AsyncSession = Depends(get_async_session)) -> List[GetGenresResponseModel]:

    statement = select(Genre)
    genres = (await session.execute(statement)).scalars().all()
    res = []
    for genre in genres:

        statement = select(Book).where(GenreToBook.book_id == Book.id, GenreToBook.genre_id == genre.id)
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

            book_model = GetGenresResponseModel.BookModel(
                id=book.id,
                title=book.title,
                genres=[
                    GetGenresResponseModel.GenreModel(
                        id=genre.id,
                        name=genre.name
                    ) for genre in genres
                ],
                rating=book_rating,
                reviews_count=reviews_count,
            )
            books_list.append(book_model)

        genre_model = GetGenresResponseModel(
            id=genre.id,
            name=genre.name,
            books=books_list
        )

        res.append(genre_model)

    # Format response
    response.status_code = status.HTTP_200_OK

    return res


@genres_router.post("/")
async def create_genre(new_genre: CreateGenreRequestModel,
                       response: Response,
                       user: User = Depends(current_user),
                       session: AsyncSession = Depends(get_async_session)) -> CreateGenreResponseModel:

    # Check for permissions (must be Admin to create genre)
    user_role = await session.get(Role, user.role_id)
    if user_role.role != Role.EnumRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to modify data"
        )

    # Genre creation
    genre = Genre(
        name=new_genre.name,
    )
    session.add(genre)

    # Committing changes
    await session.commit()

    # Format response
    response.status_code = status.HTTP_200_OK
    res = CreateGenreResponseModel(
        id=genre.id,
        name=genre.name,
    )

    return res


@genres_router.put("/{genre_id}")
async def update_genre(genre_id: int,
                       new_genre: UpdateGenreRequestModel,
                       response: Response,
                       user: User = Depends(current_user),
                       session: AsyncSession = Depends(get_async_session)) -> UpdateGenreResponseModel:

    # Check for permissions (must be Admin to update genre)
    user_role = await session.get(Role, user.role_id)
    if user_role.role != Role.EnumRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to modify data"
        )

    # Check for corresponding genre existence
    genre = await session.get(Genre, genre_id)
    if genre is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Genre with id={genre_id} can not be found"
        )

    # Updating simple fields
    genre.name = new_genre.name

    # Committing changes
    await session.commit()

    # Invalidate cache
    cache = get_cache_instance()
    cache.delete(f'/genres/{genre.id}')

    # Format response
    response.status_code = status.HTTP_200_OK
    res = UpdateGenreResponseModel(
        id=genre.id,
        name=genre.name,
    )

    return res


@genres_router.delete("/{genre_id}")
async def delete_genre(genre_id: int,
                       response: Response,
                       user: User = Depends(current_user),
                       session: AsyncSession = Depends(get_async_session)) -> DeleteGenreResponseModel:

    # Check for permissions (must be Admin to delete genre)
    user_role = await session.get(Role, user.role_id)
    if user_role.role != Role.EnumRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to modify data"
        )

    # Check for corresponding genre existence
    genre = await session.get(Genre, genre_id)
    if genre is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Genre with id={genre_id} can not be found"
        )

    # Get name before delete
    genre_name = genre.name

    # Committing changes
    await session.delete(genre)
    await session.commit()

    # Invalidate cache
    cache = get_cache_instance()
    cache.delete(f'/genres/{genre.id}')

    # Format response
    response.status_code = status.HTTP_200_OK
    res = DeleteGenreResponseModel(
        id=genre_id,
        name=genre_name
    )
    return res


