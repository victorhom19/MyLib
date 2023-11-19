import json
from datetime import datetime
from typing import List

from fastapi import APIRouter, Response, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.database import get_async_session
from cache.cache import get_cache_instance
from models.models import Review, User, Book, Role
from routes.auth_router import current_user
from routes.models.reviews.create_review_model import CreateReviewRequestModel, CreateReviewResponseModel
from routes.models.reviews.delete_review_model import DeleteReviewModelResponse
from routes.models.reviews.get_review_model import GetReviewResponseModel
from routes.models.reviews.get_reviews_model import GetReviewsResponseModel

reviews_router = APIRouter()


@reviews_router.get("/{review_id}")
async def get_review(review_id: int,
                     response: Response,
                     session: AsyncSession = Depends(get_async_session)) -> GetReviewResponseModel:

    # # Check for existing in cache
    # cache = get_cache_instance()
    # from_cache = cache.get(f'/reviews/{review_id}')
    # if from_cache is not None:
    #     return GetReviewResponseModel.parse_json(from_cache)

    # Check for corresponding review existence
    review = await session.get(Review, review_id)
    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with id={review_id} not found"
        )

    review_owner = await session.get(User, review.user_id)

    # Format response
    response.status_code = status.HTTP_200_OK
    res = GetReviewResponseModel(
        id=review.id,
        user=GetReviewResponseModel.UserModel(
            id=review_owner.id,
            name=review_owner.name
        ),
        book_id=review.book_id,
        rating=review.rating,
        text=review.text,
        created=review.created
    )

    # # Cache response
    # cache.set(f"/reviews/{review.id}", json.dumps(res.as_dict()))

    return res


@reviews_router.get("/")
async def get_reviews(response: Response,
                      session: AsyncSession = Depends(get_async_session)) -> List[GetReviewsResponseModel]:

    statement = select(Review, User).outerjoin(User, Review.user_id == User.id)
    reviews_to_users = (await session.execute(statement)).all()

    res = []
    for review, user in reviews_to_users:

        review_model = GetReviewsResponseModel(
            id=review.id,
            user=GetReviewsResponseModel.UserModel(
                id=user.id,
                name=user.name
            ),
            book_id=review.book_id,
            rating=review.rating,
            text=review.text,
            created=review.created
        )

        res.append(review_model)

    # Format response
    response.status_code = status.HTTP_200_OK

    return res


@reviews_router.post("/")
async def create_review(new_review: CreateReviewRequestModel,
                        response: Response,
                        user: User = Depends(current_user),
                        session: AsyncSession = Depends(get_async_session)) -> CreateReviewResponseModel:

    # Check for corresponding book existence
    book = await session.get(Book, new_review.book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid request payload. Book with id={new_review.book_id} does not exist"
        )

    # Check for rating constraints
    if new_review.rating < 1 or new_review.rating > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid request payload. Rating value should be between 1 and 5 inclusively"
        )

    # Review creation
    review = Review(
        user_id=user.id,
        book_id=book.id,
        rating=new_review.rating,
        text=new_review.text,
        created=datetime.now()
    )
    session.add(review)

    # Committing changes
    await session.commit()

    # Invalidate cache
    cache = get_cache_instance()
    cache.delete(f'/books/{book.id}')

    # Format response
    response.status_code = status.HTTP_200_OK
    res = CreateReviewResponseModel(
        id=review.id,
        book_id=book.id,
        user=CreateReviewResponseModel.UserModel(
            id=user.id,
            name=user.name
        ),
        rating=review.rating,
        text=review.text,
        created=review.created
    )

    return res


@reviews_router.delete("/{review_id}")
async def delete_review(review_id: int,
                        response: Response,
                        user: User = Depends(current_user),
                        session: AsyncSession = Depends(get_async_session)) -> DeleteReviewModelResponse:

    # Check for corresponding review existence
    review = await session.get(Review, review_id)
    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with id={review_id} does not exist"
        )

    # Check for permissions (must be owner of review or Moderator or Admin)
    user_role = await session.get(Role, user.role_id)
    if user.id != review.user_id and user_role.role not in (Role.EnumRole.MODERATOR, Role.EnumRole.ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to modify data"
        )

    review_owner = await session.get(User, review.user_id)
    book_id = review.book_id

    # Committing changes
    await session.delete(review)
    await session.commit()

    # # Invalidate cache
    # cache = get_cache_instance()
    # cache.delete(f'/reviews/{review_id}')
    # cache.delete(f'/books/{book_id}')

    # Format response
    response.status_code = status.HTTP_200_OK
    res = DeleteReviewModelResponse(
        id=review_id,
        user=DeleteReviewModelResponse.UserModel(
            id=review_owner.id,
            name=review_owner.name
        )
    )
    return res
