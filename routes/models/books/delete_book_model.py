from pydantic import BaseModel


class DeleteBookModelResponse(BaseModel):
    id: int
    title: str
