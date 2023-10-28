from datetime import datetime

from pydantic import BaseModel


class CreateReviewRequestModel(BaseModel):
    book_id: int
    rating: int
    text: str


class CreateReviewResponseModel(BaseModel):

    class UserModel(BaseModel):
        id: int
        name: str

    id: int
    user: UserModel
    book_id: int
    rating: int
    text: str
    created: datetime
