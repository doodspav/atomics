from typing import Generic, TypeVar


T = TypeVar('T', bytes, int)


class CmpxchgResult(Generic[T]):

    def __init__(self, success: bool, expected: T):
        self.success: bool = success
        self.expected: T = expected

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(success={self.success}, " \
               f"expected={self.expected})"

    def __bool__(self) -> bool:
        return self.success

    def __iter__(self):
        return iter((self.success, self.expected))
