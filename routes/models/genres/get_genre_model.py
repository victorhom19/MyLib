import json

from pydantic import BaseModel


class GetGenreResponseModel(BaseModel):
    id: int
    name: str

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

    @staticmethod
    def parse_json(json_repr):
        genre = json.loads(json_repr)
        return GetGenreResponseModel(
            id=int(genre['id']),
            name=genre['name']
        )
