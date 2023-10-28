import json
from typing import List

from pydantic import BaseModel

from routes.models.genres.get_genre_model import GetGenreResponseModel


class GetGenresResponseModel(BaseModel):

    class GenreModel(BaseModel):
        id: int
        name: str

    class BookModel(BaseModel):
        id: int
        title: str
        genres: List['GetGenresResponseModel.GenreModel']
        rating: float
        reviews_count: int

    id: int
    name: str
    books: List[BookModel]

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
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
        genre = json.loads(json_repr)
        return GetGenreResponseModel(
            id=int(genre['id']),
            name=genre['name'],
            books=[
                GetGenresResponseModel.BookModel(
                    id=book['id'],
                    title=book['title'],
                    genres=[
                       GetGenresResponseModel.GenreModel(
                           id=genre['id'],
                           name=genre['name']
                       ) for genre in book['genres']
                    ],
                    rating=book['rating'],
                    reviews_count=book['reviews_count']
                ) for book in genre['books']
            ]
        )