from typing import List

from pydantic import BaseModel


class UpdateAuthorRequestModel(BaseModel):
    name: str
    about: str


class UpdateAuthorResponseModel(BaseModel):
    class GenreModel(BaseModel):
        id: int
        name: str

    class BookModel(BaseModel):
        id: int
        title: str
        genres: List['UpdateAuthorResponseModel.GenreModel']
        rating: float
        reviews_count: int

    id: int
    name: str
    about: str
    books: List[BookModel]
