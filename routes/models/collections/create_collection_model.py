from typing import List

from pydantic import BaseModel


class CreateCollectionRequestModel(BaseModel):
    title: str


class CreateCollectionResponseModel(BaseModel):
    id: int
    title: str
    books: List[object]  # as it initially empty
