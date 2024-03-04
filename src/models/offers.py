from pydantic import BaseModel

from src.models.items import Item


class Offer(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    items: list[Item]
