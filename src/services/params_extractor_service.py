from typing import Self


def common_params(q: str | None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


class CommonParams:
    def __init__(
        self: Self, q: str | None = None, skip: int = 0, limit: int = 0
    ) -> None:
        self.q = q
        self.skip = skip
        self.limit = limit
