from uuid import UUID

from src.models.users import UserBase


class UserDAO(UserBase):
    id: UUID
    hashed_password: str
