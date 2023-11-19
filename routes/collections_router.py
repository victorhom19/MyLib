import json
from typing import List

from fastapi import APIRouter, Depends, status, HTTPException, Response
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.database import get_async_session
from cache.cache import get_cache_instance
from models.models import Book, User, Role, Collection, BookToCollection, Review, Genre, GenreToBook
from routes.auth_router import current_user
from routes.models.collections.create_collection_model import CreateCollectionRequestModel, \
    CreateCollectionResponseModel
from routes.models.collections.delete_collection_model import DeleteCollectionResponseModel
from routes.models.collections.get_collection_model import GetCollectionResponseModel
from routes.models.collections.get_collections_model import GetCollectionsResponseModel
from routes.models.collections.update_collection_model import UpdateCollectionRequestModel, \
    UpdateCollectionResponseModel

collections_router = APIRouter()


@collections_router.get("/{collection_id}")
async def get_collection(collection_id: int,
                         response: Response,
                         session: AsyncSession = Depends(get_async_session)) -> GetCollectionResponseModel:

    # # Check for existing in cache
    # cache = get_cache_instance()
    # from_cache = cache.get(f'/collections/{collection_id}')
    # if from_cache is not None:
    #     return GetCollectionResponseModel.parse_json(from_cache)

    collection = await session.get(Collection, collection_id)
    if collection is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Collection with id={collection_id} not found"
        )

    statement = select(Book).where(BookToCollection.book_id == Book.id, BookToCollection.collection_id == collection_id)
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

        book_model = GetCollectionResponseModel.BookModel(
            id=book.id,
            title=book.title,
            genres=[
                GetCollectionResponseModel.GenreModel(
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
    res = GetCollectionResponseModel(
        id=collection.id,
        title=collection.title,
        books=books_list
    )
    #
    # # Cache response
    # cache.set(f"/collections/{collection.id}", json.dumps(res.as_dict()))

    return res


@collections_router.get("/")
async def get_collections(response: Response,
                          user: User = Depends(current_user),
                          session: AsyncSession = Depends(get_async_session)) -> List[GetCollectionsResponseModel]:

    statement = select(Collection).where(Collection.user_id == user.id)
    collections = (await session.execute(statement)).scalars().all()
    res = []

    for collection in collections:

        statement = select(Book).where(BookToCollection.collection_id == collection.id, Book.id == BookToCollection.book_id)
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

            book_model = GetCollectionsResponseModel.BookModel(
                id=book.id,
                title=book.title,
                genres=[
                    GetCollectionsResponseModel.GenreModel(
                        id=genre.id,
                        name=genre.name
                    ) for genre in genres
                ],
                rating=book_rating,
                reviews_count=reviews_count,
            )
            books_list.append(book_model)

        collection_model = GetCollectionsResponseModel(
            id=collection.id,
            title=collection.title,
            books=books_list
        )

        res.append(collection_model)

    # Format response
    response.status_code = status.HTTP_200_OK

    return res


@collections_router.post("/")
async def create_collection(new_collection: CreateCollectionRequestModel,
                            response: Response,
                            user: User = Depends(current_user),
                            session: AsyncSession = Depends(get_async_session)) -> CreateCollectionResponseModel:

    # Collection creation
    collection = Collection(
        title=new_collection.title,
        user_id=user.id
    )
    session.add(collection)

    # Committing changes
    await session.commit()

    # Format response
    response.status_code = status.HTTP_200_OK
    res = CreateCollectionResponseModel(
        id=collection.id,
        title=collection.title,
        books=[]
    )

    return res


@collections_router.put("/{collection_id}")
async def update_collection(collection_id: int,
                            new_collection: UpdateCollectionRequestModel,
                            response: Response,
                            user: User = Depends(current_user),
                            session: AsyncSession = Depends(get_async_session)) -> UpdateCollectionResponseModel:

    # Check for corresponding collection existence
    collection = await session.get(Collection, collection_id)
    if collection is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Collection with id={collection_id} can not be found"
        )

    # Check for permissions (must be the owner of collection to update)
    if user.id != collection.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to modify data"
        )

    # Check for corresponding books existence
    statement = select(Book).where(Book.id.in_(new_collection.book_ids))
    books = (await session.execute(statement)).scalars().all()
    found_ids = [book.id for book in books]
    missing_books = [str(book_id) for book_id in new_collection.book_ids if book_id not in found_ids]
    if len(missing_books) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid request payload. Books with id={', '.join(missing_books)} do not exist"
        )

    # Updating simple fields
    collection.title = new_collection.title

    # Updating many-to-many relationships (books-genres)
    statement = select(BookToCollection).where(BookToCollection.collection_id == collection.id)
    books_to_collections = (await session.execute(statement)).scalars().all()
    for book_to_collection in books_to_collections:
        await session.delete(book_to_collection)
    for book_id in new_collection.book_ids:
        book_to_collection = BookToCollection(
            collection_id=collection.id,
            book_id=book_id
        )
        session.add(book_to_collection)

    # Committing changes
    await session.commit()

    # # Invalidate cache
    # cache = get_cache_instance()
    # cache.delete(f'/collections/{collection_id}')

    # Collect additional data about collection books
    statement = select(Book).where(BookToCollection.book_id == Book.id, BookToCollection.collection_id == collection.id)
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

        book_model = UpdateCollectionResponseModel.BookModel(
            id=book.id,
            title=book.title,
            genres=[
                UpdateCollectionResponseModel.GenreModel(
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
    res = UpdateCollectionResponseModel(
        id=collection.id,
        title=collection.title,
        books=books_list
    )

    return res

@collections_router.delete("/{collection_id}")
async def delete_collection(collection_id: int,
                            response: Response,
                            user: User = Depends(current_user),
                            session: AsyncSession = Depends(get_async_session)) -> DeleteCollectionResponseModel:

    # Check for corresponding collection existence
    collection = await session.get(Collection, collection_id)
    if collection is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Collection with id={collection_id} can not be found"
        )

    # Check for permissions (must be the owner of collection to update)
    if user.id != collection.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to modify data"
        )

    # Get title before delete
    collection_title = collection.title

    # Committing changes
    await session.delete(collection)
    await session.commit()

    # # Invalidate cache
    # cache = get_cache_instance()
    # cache.delete(f'/collections/{collection.id}')

    # Format response
    response.status_code = status.HTTP_200_OK
    res = DeleteCollectionResponseModel(
        id=collection_id,
        title=collection_title
    )
    return res