from typing import Optional
from beanie import Document


class User(Document):
    first_name: str
    last_name: str
    email: str
    password: str


class ToDos(Document):
    created_by: Optional[str]
    name: str
    desc: str