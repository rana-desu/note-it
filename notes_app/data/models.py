from flask_login import UserMixin
from dataclasses import dataclass
import datetime


@dataclass
class User(UserMixin):
    user_id: int
    username: str
    email: str
    password_hash: str
    
    @staticmethod
    def from_dict(data) -> "User":
        return User(**data)

    def get_id(self):
        return self.email


@dataclass
class Note:
    note_id: int
    owner_id: int
    title: str
    description: str
    date_created: datetime.datetime
    
    @staticmethod
    def from_dict(data) -> "Note":
        return Note(**data)
