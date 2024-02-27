from fastapi import FastAPI

from src.db.fake_db import fake_items_db
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


@app.get("/models/{name}")
async def get_model(name: ModelName):
    if name is ModelName.alexnet:
        return {"name": name, "message": "Deep Learning FTW!"}

    if name.value == "lenet":
        return {"name": name, "message": "LeCNN all the images"}

    return {"name": name, "message": "Have some residual"}

@app.get("/files/{file_path:path}")
async def get_file(file_path: str):
    return {"file_path": file_path }

@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 0):
    print('Hi', fake_items_db[skip : skip + limit])
    return fake_items_db[skip : skip + limit]
