import json
from typing import List

from pydantic import BaseModel


class GetAuthorsResponseModel(BaseModel):

    class GenreModel(BaseModel):
        id: int
        name: str

    class BookModel(BaseModel):
        id: int
        title: str
        genres: List['GetAuthorsResponseModel.GenreModel']
        rating: float
        reviews_count: int

    id: int
    name: str
    about: str
    books: List[BookModel]

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'about': self.about,
            'books': [
                {
                    'id': book.id,
                    'title': book.title,
                    'genres': [
                        {
                            'id': genre.id,
                            'name': genre.name
                        } for genre in book.genres
                    ],
                    'rating': book.rating,
                    'reviews_count': book.reviews_count
                } for book in self.books
            ]
        }

    @staticmethod
    def parse_json(json_repr):
        authors_arr = json.loads(json_repr)
        return [
            GetAuthorsResponseModel(
                id=int(author['id']),
                name=author['name'],
                about=author['about'],
                books=[
                    GetAuthorsResponseModel.BookModel(
                        id=book['id'],
                        title=book['title'],
                        genres=[
                           GetAuthorsResponseModel.GenreModel(
                               id=genre['id'],
                               name=genre['name']
                           ) for genre in book['genres']
                        ],
                        rating=book['rating'],
                        reviews_count=book['reviews_count']
                    ) for book in author['books']
                ]
            ) for author in authors_arr
        ]
