from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.database import get_async_session
from models.models import Book, User, Role, Collection, BookToCollection
from routes.auth_router import current_user


class CollectionModel(BaseModel):
    name: str
    book_ids: List[int]


collections_router = APIRouter()


@collections_router.get("/collections/{collection_id}")
async def get_collection(collection_id: int,
                         session: AsyncSession = Depends(get_async_session)):
    collection = await session.get(Collection, collection_id)

    statement = select(BookToCollection, Book)\
        .outerjoin(Book, Book.id == BookToCollection.book_id)\
        .where(BookToCollection.collection_id == collection.id)
    books = [el[1] for el in (await session.execute(statement)).all()]
    return {
        "id": collection.id,
        "name": collection.name,
        "books": [
            {
                "id": book.id,
                "name": book.name,
                "year": book.year,
                "annotation": book.annotation
            } for book in books
        ]
    }


@collections_router.get("/collections")
async def get_collections(user: User = Depends(current_user),
                          session: AsyncSession = Depends(get_async_session)):
    statement = select(Collection).where(Collection.user_id == user.id)
    collections = (await session.execute(statement)).scalars().all()

    collection_list = []
    for collection in collections:
        statement = select(BookToCollection, Book) \
            .outerjoin(Book, Book.id == BookToCollection.book_id) \
            .where(BookToCollection.collection_id == collection.id)
        books = [el[1] for el in (await session.execute(statement)).all()]

        collection_dict = {
            "id": collection.id,
            "name": collection.name,
            "books": [
                {
                    "id": book.id,
                    "name": book.name,
                    "year": book.year,
                    "annotation": book.annotation
                } for book in books
            ]
        }
        collection_list.append(collection_dict)

    return collection_list


@collections_router.post("/collections")
async def create_collection(new_collection: CollectionModel,
                            user: User = Depends(current_user),
                            session: AsyncSession = Depends(get_async_session)):
    collection = Collection(
        name=new_collection.name,
        user_id=user.id
    )
    session.add(collection)
    await session.commit()
    for book_id in new_collection.book_ids:

        book_to_collection = BookToCollection(
            collection_id=collection.id,
            book_id=book_id
        )
        session.add(book_to_collection)
    await session.commit()
    return collection


@collections_router.put("/collections/{collection_id}")
async def update_collection(collection_id: int, new_collection: CollectionModel,
                            user: User = Depends(current_user),
                            session: AsyncSession = Depends(get_async_session)):
    user_role = await session.get(Role, user.role_id)
    collection = await session.get(Collection, collection_id)
    if user_role.role != Role.EnumRole.ADMIN or collection.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    collection.name = new_collection.name
    statement = select(BookToCollection).where(BookToCollection.collection_id == collection.id)
    books_to_collection = (await session.execute(statement)).scalars().all()
    for book_to_collection in books_to_collection:
        await session.delete(book_to_collection)
    for book_id in new_collection.book_ids:
        book_to_collection = BookToCollection(
            collection_id=collection.id,
            book_id=book_id
        )
        session.add(book_to_collection)
    await session.commit()
    return collection


@collections_router.delete("/collections/{collection_id}")
async def delete_collection(collection_id: int,
                            user: User = Depends(current_user),
                            session: AsyncSession = Depends(get_async_session)):
    user_role = await session.get(Role, user.role_id)
    collection = await session.get(Collection, collection_id)
    if user_role.role != Role.EnumRole.ADMIN or collection.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    collection = await session.get(Collection, collection_id)
    await session.delete(collection)
    await session.commit()
    return {'removed': collection_id}
