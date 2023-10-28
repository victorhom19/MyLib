from pydantic import BaseModel


class DeleteGenreResponseModel(BaseModel):
    id: int
    name: str
