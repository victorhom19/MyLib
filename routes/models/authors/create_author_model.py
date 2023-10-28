from typing import List

from pydantic import BaseModel


class CreateAuthorRequestModel(BaseModel):
    name: str
    about: str


class CreateAuthorResponseModel(BaseModel):
    id: int
    name: str
    about: str
    books: List[object]  # As initially it is empty
