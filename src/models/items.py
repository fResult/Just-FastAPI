from uuid import UUID

from pydantic import BaseModel

from src.models.images import Image


class Item(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    images: list[Image] | None = None
