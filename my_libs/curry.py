from typing import Callable, TypeVar, overload
from functools import reduce

T = TypeVar("T")
T1 = TypeVar("T1")
T2 = TypeVar("T2")
T3 = TypeVar("T3")
T4 = TypeVar("T4")
T5 = TypeVar("T5")
T6 = TypeVar("T6")
T7 = TypeVar("T7")
R = TypeVar("R")


def identity(x: T1) -> T1:
    return x


@overload
def compose(f1: Callable[[T1], T2]) -> Callable[[T1], T2]:
    ...


@overload
def compose(
    f2: Callable[[T2], T3],
    f1: Callable[[T1], T2],
) -> Callable[[T1], T3]:
    ...


@overload
def compose(
    f3: Callable[[T3], T4],
    f2: Callable[[T2], T3],
    f1: Callable[[T1], T2],
) -> Callable[[T1], T4]:
    ...


@overload
def compose(
    f4: Callable[[T4], T5],
    f3: Callable[[T3], T4],
    f2: Callable[[T2], T3],
    f1: Callable[[T1], T2],
) -> Callable[[T1], T5]:
    ...


@overload
def compose(
    f5: Callable[[T5], T6],
    f4: Callable[[T4], T5],
    f3: Callable[[T3], T4],
    f2: Callable[[T2], T3],
    f1: Callable[[T1], T2],
) -> Callable[[T1], T6]:
    ...


@overload
def compose(
    f6: Callable[[T6], T7],
    f5: Callable[[T5], T6],
    f4: Callable[[T4], T5],
    f3: Callable[[T3], T4],
    f2: Callable[[T2], T3],
    f1: Callable[[T1], T2],
) -> Callable[[T1], T7]:
    ...


@overload
def compose(
    f7: Callable[[R], T7],
    f6: Callable[[T6], T7],
    f5: Callable[[T5], T6],
    f4: Callable[[T4], T5],
    f3: Callable[[T3], T4],
    f2: Callable[[T2], T3],
    f1: Callable[[T1], T2],
) -> Callable[[T1], T7]:
    ...


def compose(*funcs: Callable) -> Callable:
    def compose_two(f: Callable, g: Callable) -> Callable:
        return lambda x: f(g(x))

    return reduce(compose_two, funcs, identity)


## Test zone
def twice(x: int) -> int:
    return x * 2


def sqr(x: int) -> float:
    return x ** 2


def is_odd(x: int) -> bool:
    return x % 2 != 0


def mymap(f: Callable[[T1], T2]) -> Callable[[list[T1]], list[T2]]:
    return lambda xs: [f(x) for x in xs]


def myfilter(f: Callable[[T1], bool]) -> Callable[[list[T1]], list[T1]]:
    return lambda xs: [x for x in xs if f(x)]


times_4 = compose(twice, twice)
twice_only_if_odd = compose(mymap(twice), myfilter(is_odd))

times_4(8)  # 32
twice_only_if_odd([1, 2, 3, 4, 5, 6, 7, 8, 9])  # [2, 6, 10, 14, 18]
mymap(compose(sqr, twice))([1, 2, 3, 4, 5, 6, 7, 8, 9]) # [4, 16, 36, 64, 100, 144, 196, 256, 324]
