from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field

from src.models.images import Image


class ItemCreationRequest(BaseModel):
    name: str = Field(examples=["Foo"])
    description: str | None = Field(
        default=None,
        max_length=300,
        examples=["A very nice item"],
    )
    price: float = Field(
        gt=0,
        description="The price must be greater than zero",
        examples=[35.4],
    )
    tax: Annotated[float | None, Field(default=None, examples=[3.2])] = None
    tags: set[str] = Field(default=set(), examples=[["Foo", "Zilla"]])
    images: list[Image] | None = Field(
        default=None,
        examples=[
            [
                {"name": "img-1", "url": "https://example.com/"},
                {"name": "img-2", "url": "https://example.com/"},
            ]
        ],
    )


class ItemUpdateRequest(ItemCreationRequest):
    pass


class ItemCreation(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    price_with_tax: float
    tags: set[str] = set()
    images: list[Image] | None = None


class ItemUpdate(ItemCreation):
    q: str | None = None


class ItemCreationResponse(BaseModel):
    created_item: ItemCreation


class ItemUpdateResponse(BaseModel):
    updated_item: ItemUpdate | None
