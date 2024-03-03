from pydantic import BaseModel, Field
from src.models.images import Image


class ItemCreationRequest(BaseModel):
    name: str
    description: str | None = Field(default=None, max_length=300)
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] | None = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Foo",
                "description": "Here is your description!",
                "price": 99.99,
                "tax": 8.8,
                "tags": ["Korn", "Zilla"],
                "images": [
                    {"name": "img-1", "url": "https://example.com/"},
                    {"name": "img-2", "url": "https://example.com/"},
                ],
            }
        }
    }


class ItemUpdateRequest(ItemCreationRequest):
    pass


class ItemCreation(BaseModel):
    id: int
    name: str
    description: str | None = None
    price_with_tax: float
    tags: set[str] = set()
    images: list[Image] | None = None


class ItemUpdate(ItemCreation):
    q: str | None = None
    pass


class ItemCreationResponse(BaseModel):
    created_item: ItemCreation


class ItemUpdateResponse(BaseModel):
    updated_item: ItemUpdate | None
