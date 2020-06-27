from .base import BaseObject
from classforge import Class, Field

class Device(BaseObject):

    name = Field(type=str, required=True)

    def to_dict(self):
        return dict(
            name = self.name
        )

    @classmethod
    def from_dict(cls, song, data):
        return Device(
            name = data['name']
        )