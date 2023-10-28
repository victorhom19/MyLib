import json
from datetime import datetime

from pydantic import BaseModel


class GetReviewsResponseModel(BaseModel):

    class UserModel(BaseModel):
        id: int
        name: str

    id: int
    user: UserModel
    book_id: int
    rating: int
    text: str
    created: datetime

    def as_dict(self):
        return {
            'id': self.id,
            'user': {
                'id': self.user.id,
                'name': self.user.name
            },
            'book_id': self.book_id,
            'rating': self.rating,
            'text': self.text,
            'created': str(self.created)
        }

    @staticmethod
    def parse_json(json_repr):
        reviews = json.loads(json_repr)
        return [
            GetReviewsResponseModel(
                id=int(review['id']),
                user=GetReviewsResponseModel.UserModel(
                    id=review['user']['id'],
                    name=review['user']['name']
                ),
                book_id=int(review['book_id']),
                rating=int(review['rating']),
                text=review['text'],
                created=review['created']
            ) for review in reviews
        ]
