from pydantic import BaseModel, Field


class ItemCreationRequest(BaseModel):
    name: str
    description: str | None = Field(default=None, max_length=300)
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None
    tags: set[str] = set()


class ItemUpdateRequest(ItemCreationRequest):
    pass


class ItemCreation(BaseModel):
    id: int
    name: str
    description: str | None = None
    price_with_tax: float
    tags: set[str] = set()


class ItemUpdate(ItemCreation):
    q: str | None = None
    pass


class ItemCreationResponse(BaseModel):
    created_item: ItemCreation


class ItemUpdateResponse(BaseModel):
    updated_item: ItemUpdate | None
