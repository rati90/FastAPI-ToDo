from typing import Union
from .documents import User


async def get_user(email: str) -> Union[User, None]:
    return await User.find_one(User.email == email)
