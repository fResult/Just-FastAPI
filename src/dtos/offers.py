from pydantic import BaseModel

from src.models.items import Item


class OfferCreationRequest(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]


class OfferCreation(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    items: list[Item]


class OfferCreationResponse(BaseModel):
    created_offer: OfferCreation
