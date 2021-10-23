from pydantic import BaseModel


class UserOut(BaseModel):
    first_name: str
    last_name: str
    email: str


class ToDo(BaseModel):
    name: str
    desc: str