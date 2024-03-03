from pydantic import BaseModel, HttpUrl


class ImageCreationRequest(BaseModel):
    name: str
    url: HttpUrl
