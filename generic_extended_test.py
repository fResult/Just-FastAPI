import logging
from typing import Callable


class Mapper[T, R]:
    val: T

    def __init__(self, val: T):
        self.val = val

    def map(self, mapper_func: Callable[[T], R]) -> R:
        return mapper_func(self.val)


class MapperWithLogging[T, R](Mapper[T, R]):
    def __init__(self, val: T):
        logging.info(f"Mapper is init with value {val}")
        super().__init__(val)

    def map(self, mapper_func: Callable[[T], R]) -> R:
        result = super().map(mapper_func)
        logging.info(f"Mapper is mapping value {self.val} to {result}")

        return result

to_int = int
mapper = MapperWithLogging[str, int]("42")
mapper.map(to_int)
