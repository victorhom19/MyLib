import json
from datetime import datetime
from typing import List

from pydantic import BaseModel


class GetBookResponseModel(BaseModel):

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
        user: 'GetBookResponseModel.UserModel'
        rating: int
        text: str
        created: datetime

    id: int
    title: str
    author: AuthorModel
    genres: List[GenreModel]
    rating: float
    reviews_count: int
    reviews: List[ReviewModel]
    year: int
    annotation: str

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
                    'created': str(review.created)
                } for review in self.reviews
            ],
            'year': self.year,
            'annotation': self.annotation
        }


    @staticmethod
    def parse_json(json_repr):
        book = json.loads(json_repr)
        return GetBookResponseModel(
            id=int(book['id']),
            title=book['title'],
            author=GetBookResponseModel.AuthorModel(
                id=int(book['author']['id']),
                name=book['author']['name']
            ),
            genres=[
                GetBookResponseModel.GenreModel(
                    id=int(genre['id']),
                    name=genre['name']
                ) for genre in book['genres']
            ],
            rating=float(book['rating']),
            reviews_count=int(book['reviews_count']),
            reviews=[
                GetBookResponseModel.ReviewModel(
                    id=int(review['id']),
                    user=GetBookResponseModel.UserModel(
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
        )