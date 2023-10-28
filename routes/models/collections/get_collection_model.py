import json
from typing import List

from pydantic import BaseModel


class GetCollectionResponseModel(BaseModel):

    class GenreModel(BaseModel):
        id: int
        name: str

    class BookModel(BaseModel):
        id: int
        title: str
        genres: List['GetCollectionResponseModel.GenreModel']
        rating: float
        reviews_count: int

    id: int
    title: str
    books: List[BookModel]

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
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
        collection = json.loads(json_repr)
        return GetCollectionResponseModel(
            id=int(collection['id']),
            title=collection['title'],
            books=[
                GetCollectionResponseModel.BookModel(
                    id=book['id'],
                    title=book['title'],
                    genres=[
                       GetCollectionResponseModel.GenreModel(
                           id=genre['id'],
                           name=genre['name']
                       ) for genre in book['genres']
                    ],
                    rating=book['rating'],
                    reviews_count=book['reviews_count']
                ) for book in collection['books']
            ]
        )
