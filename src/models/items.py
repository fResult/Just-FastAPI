from pydantic import BaseModel
from src.models.images import Image


class Item(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    image: Image | None = None
