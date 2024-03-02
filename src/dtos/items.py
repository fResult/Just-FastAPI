from pydantic import BaseModel
from typing import TypeAlias


class ItemCreationRequest(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class ItemUpdateRequest(ItemCreationRequest):
    pass


class ItemCreation(BaseModel):
    id: int
    name: str
    description: str | None = None
    price_with_tax: float


class ItemUpdate(ItemCreation):
    q: str | None = None
    pass


class ItemCreationResponse(BaseModel):
    created_item: ItemCreation


class ItemUpdateResponse(BaseModel):
    updated_item: ItemUpdate | None
