from fastapi import FastAPI
from typing import Dict

from src.db.fake_db import fake_items_db
from src.models.model_name import ModelName
from src.models.items import Item
from src.dtos.items import ItemCreationRequest, ItemCreationResponse, ItemUpdateResponse, ItemCreation

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
async def read_items(skip: int = 0, limit: int = 0):
    no_limited = limit == 0
    return fake_items_db[skip : len(fake_items_db) if no_limited else skip + limit]


@app.get("/items/{id}")
async def read_item(id: str, q: str | None = None, short: bool = False):
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
async def update_item(id: int, item: ItemCreationRequest) -> ItemUpdateResponse:
    item_dict = item.model_dump()

    price_with_tax = item.price + (item.tax if item.tax else 0)
    item_dict.update({"id": id, "price_with_tax": price_with_tax})

    return {"updated_item": ItemCreation(**item_dict)}
