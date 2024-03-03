from pydantic import BaseModel, HttpUrl


class Image(BaseModel):
    name: str
    url: HttpUrl
