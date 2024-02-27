from pydantic import BaseModel


class ItemCreationRequest(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class ItemCreation(BaseModel):
    id: int
    name: str
    description: str | None = None
    price_with_tax: float


class ItemCreationResponse(BaseModel):
    created_item: ItemCreation
