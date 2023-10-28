from pydantic import BaseModel


class DeleteCollectionResponseModel(BaseModel):
    id: int
    title: str