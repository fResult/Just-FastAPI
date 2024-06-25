from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.models.users import User

oauth2_scheme = OAuth2PasswordBearer("/users/auth")


def __fake_user_decode_token(token: str) -> User:
    return User(
        username=f"{token} fakedecode",
        email="john.doe@example.com",
        full_name="John Doe",
        disabled=False,
    )

def get_current_user(token: str, current_user: Annotated[User, Depends(oauth2_scheme)]) -> User:
    return __fake_user_decode_token(token)