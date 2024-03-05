from uuid import UUID

from pydantic import BaseModel, EmailStr

from src.models.users import UserBase


class UserCreationRequest(UserBase):
    password: str


class UserCreation(UserBase):
    id: UUID


class UserCreationResponse(BaseModel):
    created_user: UserCreation
