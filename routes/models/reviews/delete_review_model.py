from pydantic import BaseModel


class DeleteReviewModelResponse(BaseModel):

    class UserModel(BaseModel):
        id: int
        name: str

    id: int
    user: UserModel
