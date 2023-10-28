from pydantic import BaseModel


class UpdateGenreRequestModel(BaseModel):
    name: str


class UpdateGenreResponseModel(BaseModel):
    id: int
    name: str
