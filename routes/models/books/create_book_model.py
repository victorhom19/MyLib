from typing import List

from pydantic import BaseModel


class CreateBookRequestModel(BaseModel):
    title: str
    author_id: int
    genre_ids: List[int]
    year: int
    annotation: str


class CreateBookResponseModel(BaseModel):

    class AuthorModel(BaseModel):
        id: int
        name: str

    class GenreModel(BaseModel):
        id: int
        name: str

    id: int
    title: str
    author: AuthorModel
    genres: List[GenreModel]
    rating: int
    reviews_count: int
    year: int
    annotation: str
