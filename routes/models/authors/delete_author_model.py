from pydantic import BaseModel


class DeleteAuthorResponseModel(BaseModel):
    id: int
    name: str
