from statistics import mean

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.openapi.models import Response
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from auth.database import get_async_session
from models.models import Book, Author, User, Role, Review
from routes.auth_router import current_user


class AuthorModel(BaseModel):
    name: str


authors_router = APIRouter()


@authors_router.get("/authors/{author_id}")
async def get_author(author_id: int,
                     session: AsyncSession = Depends(get_async_session)):
    author = await session.get(Author, author_id)

    statement = select(Book).where(Book.author_id == author.id)
    books = (await session.execute(statement)).scalars().all()

    return {
        "id": author.id,
        "name": author.name,
        "books": [
            {
                "id": book.id,
                "name": book.name,
                "year": book.year,
                "annotation": book.annotation
            } for book in books
        ]
    }


@authors_router.get("/authors")
async def get_authors(session: AsyncSession = Depends(get_async_session)):
    statement = select(Author)
    authors = (await session.execute(statement)).scalars().all()

    author_list = []
    for author in authors:
        statement = select(Book).where(Book.author_id == author.id)
        books = (await session.execute(statement)).scalars().all()

        author_dict = {
            "id": author.id,
            "name": author.name,
            "books": [
                {
                    "id": book.id,
                    "name": book.name,
                    "year": book.year,
                    "annotation": book.annotation
                } for book in books
            ]
        }
        author_list.append(author_dict)

    return author_list


@authors_router.post("/authors")
async def create_author(new_author: AuthorModel,
                      user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):
    user_role = await session.get(Role, user.role_id)
    if user_role.role != Role.EnumRole.ADMIN:
        return None
    book = Author(
        name=new_author.name
    )
    session.add(book)
    await session.commit()
    return book


@authors_router.put("/authors/{author_id}")
async def update_author(author_id: int, new_book: AuthorModel,
                        user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):
    user_role = await session.get(Role, user.role_id)
    if user_role.role != Role.EnumRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    author = await session.get(Author, author_id)
    author.name = new_book.name
    await session.commit()
    return author


@authors_router.delete("/authors/{author_id}")
async def delete_author(author_id: int,
                        user: User = Depends(current_user),
                        session: AsyncSession = Depends(get_async_session)):
    user_role = await session.get(Role, user.role_id)
    if user_role.role != Role.EnumRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    author = await session.get(Author, author_id)
    await session.delete(author)
    await session.commit()
    return {'removed': author_id}
