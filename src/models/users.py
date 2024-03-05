from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    password: str
    email: EmailStr


class User(UserBase):
    id: UUID
    full_name: str | None = None
