from fastapi import Cookie, Depends
from typing import Annotated, Self


def common_params(q: str | None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


class CommonParams:
    def __init__(
        self: Self, q: str | None = None, skip: int = 0, limit: int = 0
    ) -> None:
        self.q = q
        self.skip = skip
        self.limit = limit


def query_extractor(q: str | None = None):
    return q


def query_or_cookie_extractor(
    q: Annotated[str, Depends(query_extractor)],
    last_query: Annotated[str | None, Cookie()] = None,
):
    if not q:
        return last_query

    return q
