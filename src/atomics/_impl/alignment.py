from .exceptions import UnsupportedWidthException
from .patomic import Patomic
from .pybuffer import PyBuffer


class Alignment:

    def __init__(self, width: int):
        # check that the width is supported
        p = Patomic()
        ops = p.ops(width)
        if p.count_nonnull_ops(ops, readonly=True) == 0:
            raise UnsupportedWidthException(width, readonly=True)
        # get alignment info
        align = p.alignment(width)
        self.width: int = width
        self.recommended: int = align.recommended
        self.minimum: int = align.minimum
        self.size_within: int = align.size_within

    def __str__(self):
        msg = f"{self.__class__.__name__}(width={self.width}, " \
              f"recommended={self.recommended}, minimum=" \
              f"{self.minimum}, size_within={self.size_within})"
        return msg

    @staticmethod
    def buffer_address(buffer) -> int:
        try:
            with memoryview(buffer) as view:
                return PyBuffer(view, writeable=False).address
        except TypeError:
            error_msg = "Positional argument 'buffer' must support the " \
                        "buffer protocol."
        raise TypeError(error_msg)

    def is_valid_recommended(self, address: int) -> bool:
        if address < 0:
            raise ValueError("Address is negative")
        return (address % self.recommended) == 0

    def is_valid_minimum(self, address: int) -> bool:
        if address < 0:
            raise ValueError("Address is negative")
        if (address % self.minimum) == 0:
            if self.size_within == 0:
                return True
            else:
                address %= self.size_within
                return (address + self.width) <= self.size_within
        else:
            return False

    def is_valid(self, address: int, *, using_recommended: bool = True) -> bool:
        if using_recommended:
            return self.is_valid_recommended(address)
        else:
            return self.is_valid_minimum(address)
