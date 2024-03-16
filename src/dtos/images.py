from pydantic import BaseModel, HttpUrl


class ImageCreationRequest(BaseModel):
    name: str | None = None
    url: HttpUrl
