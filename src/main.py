from typing import Annotated
from uuid import UUID

from fastapi import Body, Cookie, FastAPI, Path, Query

from src.db.fake_db import fake_items_db
from src.dtos.images import ImageCreationRequest
from src.dtos.items import (
    ItemCreation,
    ItemCreationRequest,
    ItemCreationResponse,
    ItemUpdate,
    ItemUpdateRequest,
    ItemUpdateResponse,
)
from src.dtos.offers import OfferCreation, OfferCreationRequest, OfferCreationResponse
from src.models.model_name import ModelName

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/users/me")
async def read_my_user():
    return {"id": "current user"}


@app.get("/users/{id}")
async def read_user(id: str):
    return {"id": id}


@app.get("users/{id}/items/{item_id}")
async def read_user_item(
    user_id: str, item_id: str, q: str | None = None, short: bool = False
):
    item = {"id": item_id, "owner_id": user_id}

    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {
                "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Velit ad accusantium quae nihil vero quas rerum! Tempora, eos exercitationem. Velit animi odit molestiae, architecto dolorem vitae corporis ea porro provident."
            }
        )

    return item


@app.get("/models/{name}")
async def get_model(name: ModelName):
    if name is ModelName.alexnet:
        return {"name": name, "message": "Deep Learning FTW!"}

    if name.value == "lenet":
        return {"name": name, "message": "LeCNN all the images"}

    return {"name": name, "message": "Have some residual"}


@app.get("/files/{file_path:path}")
async def get_file(file_path: str):
    return {"file_path": file_path}


@app.get("/items/")
async def read_items(
    ads_id: Annotated[str | None, Cookie()] = None,
    skip: int = 0,
    limit: int = 0,
    item_query: Annotated[
        str,
        Query(
            alias="item-query",
            title="Query String",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            max_length=50,
            pattern="(?i)^select.*from.*;$",
            deprecated=True,
        ),
    ] = "SELECT first_name, last_name FROM persons /* It's just example */;",
    hidden_query: Annotated[
        str | None, Query(include_in_schema=False, alias="hidden-query")
    ] = None,
):
    no_limited = limit == 0
    results = {"items": fake_items_db}

    print("cookie", ads_id)

    results.update(
        {
            "items": fake_items_db[
                skip : len(fake_items_db) if no_limited else skip + limit
            ],
        }
    )

    if item_query:
        results.update({"q": item_query})

    if hidden_query:
        results.update({"hidden_query": hidden_query})
    else:
        results.update({"hidden_query": "Not found"})

    return results


@app.get("/items/qs")
async def read_items_with_queries(
    q: Annotated[list[str], Query(title="Query String", min_length=3)] = [],
):
    query_items = {"q": q}
    return query_items


@app.get("/items/{id}")
async def read_item(
    id: Annotated[
        UUID,
        Path(
            title="ID for the item to get",
            example="018e0aa8-48a9-7ae4-9746-1dc89c3f70cd",
            openapi_examples={
                "normal": {
                    "summary": "Normal UUID",
                    "value": "018e0aa8-48a9-7ae4-9746-1dc89c3f70cd",
                },
                "invalid": {
                    "summary": "Invalid UUID",
                    "value": "wrong-uuid",
                },
            },
        ),
    ],
    q: Annotated[str | None, Query(alias="item-query")] = None,
    short: bool = False,
):
    item = {"id": id}

    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {
                "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Velit ad accusantium quae nihil vero quas rerum! Tempora, eos exercitationem. Velit animi odit molestiae, architecto dolorem vitae corporis ea porro provident."
            }
        )

    return item


@app.post("/items/")
async def create_item(
    item: ItemCreationRequest,
) -> ItemCreationResponse:
    item_dict = item.model_dump()

    price_with_tax = item.price + (item.tax if item.tax else 0)
    item_dict.update({"id": 1, "price_with_tax": price_with_tax})

    return {"created_item": ItemCreation(**item_dict)}


@app.put("/items/{id}")
async def update_item(
    id: UUID,
    item: Annotated[
        ItemUpdateRequest | None,
        Body(
            openapi_examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "name": "Bar",
                        "description": "A very nice item",
                        "price": 35.4,
                        "tax": 3.2,
                        "tags": ["Bar", "Zilla"],
                        "images": [
                            {"name": "img-1", "url": "https://example.com/"},
                            {"name": "img-2", "url": "https://example.com/"},
                        ],
                    },
                },
                "converted": {
                    "summary": "An example with converted data",
                    "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                    "value": {
                        "name": "Baz",
                        "price": "35.4",
                        "tags": [],
                    },
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "name": "Baz",
                        "price": "thirty five point four",
                        "tags": [],
                    },
                },
            }
        ),
    ] = None,
    q: str | None = None,
) -> ItemUpdateResponse:
    if not item:
        return {"updated_item": None}

    item_dict = item.model_dump()

    price_with_tax = item.price + (item.tax if item.tax else 0)
    item_dict.update({"id": id, "price_with_tax": price_with_tax})

    if q:
        item_dict = {"q": q, **item_dict}

    return {"updated_item": ItemUpdate(**item_dict)}


@app.post("/offers/")
async def create_offer(offer: OfferCreationRequest) -> OfferCreationResponse:
    offer_dict = offer.model_dump()

    offer_dict.update({"id": 12})

    return {"created_offer": OfferCreation(**offer_dict)}


@app.post("/images/multiple/")
async def create_multiple_images(images: list[ImageCreationRequest]):
    print([img.model_dump() for img in images])
    return images
