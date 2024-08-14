from typing import Callable, overload
from functools import reduce

def identity[T](x: T) -> T:
    return x


@overload
def compose[T, R](f: Callable[[T], R]) -> Callable[[T], R]:
    ...


@overload
def compose[T1, T2, R](
    f2: Callable[[T2], R],
    f1: Callable[[T1], T2],
) -> Callable[[T1], R]:
    ...


@overload
def compose[T1, T2, T3, R](
    f3: Callable[[T3], R],
    f2: Callable[[T2], T3],
    f1: Callable[[T1], T2],
) -> Callable[[T1], R]:
    ...


@overload
def compose[T1, T2, T3, T4, R](
    f4: Callable[[T4], R],
    f3: Callable[[T3], T4],
    f2: Callable[[T2], T3],
    f1: Callable[[T1], T2],
) -> Callable[[T1], R]:
    ...


@overload
def compose[T1, T2, T3, T4, T5, R](
    f5: Callable[[T5], R],
    f4: Callable[[T4], T5],
    f3: Callable[[T3], T4],
    f2: Callable[[T2], T3],
    f1: Callable[[T1], T2],
) -> Callable[[T1], R]:
    ...


@overload
def compose[T1, T2, T3, T4, T5, T6, R](
    f6: Callable[[T6], R],
    f5: Callable[[T5], T6],
    f4: Callable[[T4], T5],
    f3: Callable[[T3], T4],
    f2: Callable[[T2], T3],
    f1: Callable[[T1], T2],
) -> Callable[[T1], R]:
    ...


@overload
def compose[T1, T2, T3, T4, T5, T6, T7, R](
    f7: Callable[[T7], R],
    f6: Callable[[T6], T7],
    f5: Callable[[T5], T6],
    f4: Callable[[T4], T5],
    f3: Callable[[T3], T4],
    f2: Callable[[T2], T3],
    f1: Callable[[T1], T2],
) -> Callable[[T1], R]:
    ...


def compose(*funcs: Callable) -> Callable: # type: ignore
    def compose_two(f: Callable, g: Callable) -> Callable[[object], object]:
        return lambda x: g(f(x))
    fns = list(funcs).copy()

    return reduce(compose_two, reversed(fns), identity)


## Test zone
def twice(x: int) -> int:
    return x * 2


def sqr(x: int) -> float:
    return x ** 2


def is_odd(x: int) -> bool:
    return x % 2 != 0


def mymap[T, R](f: Callable[[T], R]) -> Callable[[list[T]], list[R]]:
    return lambda xs: [f(x) for x in xs]


def myfilter[T](f: Callable[[T], bool]) -> Callable[[list[T]], list[T]]:
    return lambda xs: [x for x in xs if f(x)]


times_4 = compose(twice, twice)
twice_only_if_odd = compose(mymap(twice), myfilter(is_odd))

times_4(8)  # 32
twice_only_if_odd([1, 2, 3, 4, 5, 6, 7, 8, 9])  # [2, 6, 10, 14, 18]
print(mymap(compose(sqr, twice))([1, 2, 3, 4, 5, 6, 7, 8, 9])) # [4, 16, 36, 64, 100, 144, 196, 256, 324]
print(times_4(8))
