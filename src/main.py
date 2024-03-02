from fastapi import FastAPI, Query, Path, Body
from typing import Annotated

from src.db.fake_db import fake_items_db
from src.models.model_name import ModelName
from src.models.items import Item
from src.dtos.items import (
    ItemCreationRequest,
    ItemUpdateRequest,
    ItemCreationResponse,
    ItemUpdateResponse,
    ItemCreation,
    ItemUpdate,
)

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
    id: Annotated[int, Path(title="ID for the item to get", ge=1, lt=1000)],
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
    id: int,
    item: ItemUpdateRequest | None = None,
    q: str | None = None,
    importance: Annotated[int, Body()] = 5,
) -> ItemUpdateResponse:
    print(not item, importance)
    if not item:
        return {"updated_item": None}

    item_dict = item.model_dump()

    price_with_tax = item.price + (item.tax if item.tax else 0)
    item_dict.update({"id": id, "price_with_tax": price_with_tax})

    if q:
        item_dict = {"q": q, **item_dict}

    return {"updated_item": ItemUpdate(**item_dict)}
