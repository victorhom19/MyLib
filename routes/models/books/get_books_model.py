import json
from typing import List, Union

from pydantic import BaseModel


class GetBooksRequestModel(BaseModel):
    search_query: Union[None, str]
    genre_ids: Union[None, List[int]]
    year_from: Union[None, int]
    year_to: Union[None, int]
    author_ids: Union[None, List[int]]


class GetBooksResponseModel(BaseModel):

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
    rating: float
    reviews_count: int

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': {
                'id': self.author.id,
                'name': self.author.name,
            },
            'genres': [
                {
                    'id': genre.id,
                    'name': genre.name
                } for genre in self.genres
            ],
            'rating': self.rating,
            'reviews_count': self.reviews_count,
            'reviews': [
                {
                    'id': review.id,
                    'user': {
                        'id': review.user.id,
                        'name': review.user.name
                    },
                    'rating': review.rating,
                    'text': review.text,
                    'created': review.created
                } for review in self.reviews
            ],
            'year': self.year,
            'annotation': self.annotation
        }

    @staticmethod
    def parse_json(json_repr):
        books = json.loads(json_repr)
        return [
            GetBooksResponseModel(
                id=int(book['id']),
                title=book['title'],
                author=GetBooksResponseModel.AuthorModel(
                    id=int(book['author']['id']),
                    name=book['author']['name']
                ),
                genres=[
                    GetBooksResponseModel.GenreModel(
                        id=int(genre['id']),
                        name=genre['name']
                    ) for genre in book['genres']
                ],
                rating=float(book['rating']),
                reviews_count=int(book['reviews_count']),
                reviews=[
                    GetBooksResponseModel.ReviewModel(
                        id=int(review['id']),
                        user=GetBooksResponseModel.UserModel(
                            id=int(review['user']['id']),
                            name=review['user']['name'],
                        ),
                        rating=int(review['rating']),
                        text=review['text'],
                        created=review['created'],
                    ) for review in book['reviews']
                ],
                year=int(book['year']),
                annotation=book['annotation']
            ) for book in books
        ]