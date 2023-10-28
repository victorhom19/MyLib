from pydantic import BaseModel


class CreateGenreRequestModel(BaseModel):
    name: str


class CreateGenreResponseModel(BaseModel):
    id: int
    name: str
