from datetime import datetime
from typing import List

from pydantic import BaseModel


class UpdateBookRequestModel(BaseModel):
    title: str
    author_id: int
    genre_ids: List[int]
    year: int
    annotation: str


class UpdateBookResponseModel(BaseModel):

    class UserModel(BaseModel):
        id: int
        name: str

    class AuthorModel(BaseModel):
        id: int
        name: str

    class GenreModel(BaseModel):
        id: int
        name: str

    class ReviewModel(BaseModel):
        id: int
        user: 'UpdateBookResponseModel.UserModel'
        rating: int
        text: str
        created: datetime

    id: int
    title: str
    author: AuthorModel
    genres: List[GenreModel]
    rating: int
    reviews_count: int
    reviews: List[ReviewModel]
    year: int
    annotation: str
