from .exceptions import UnsupportedWidthException
from .patomic import Patomic
from .pybuffer import PyBuffer


class Alignment:

    def __init__(self, width: int):
        # check that the width is supported
        p = Patomic()
        ops = p.ops(width)
        if p.count_nonnull_ops(ops, readonly=False) == 0:
            raise UnsupportedWidthException(width, readonly=False)
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

    def _checked_buffer(self, buffer) -> PyBuffer:
        # check support for buffer protocol
        try:
            pybuf = PyBuffer(buffer, writeable=False)
            # check width
            if len(pybuf) != self.width:
                error_msg = "Positional argument 'buffer' does not have" \
                            f" matching width of {self.width}."
                raise ValueError(error_msg)
            # return for use in validation functions
            return pybuf
        except TypeError:
            pass
        # caught TypeError (raise here instead of within except context)
        error_msg = "Positional argument 'buffer' must support the " \
                    "buffer protocol."
        raise TypeError(error_msg)

    def is_valid(self, buffer, *, using_recommended: bool = True) -> bool:
        with self._checked_buffer(buffer) as pybuf:
            # recommended
            if using_recommended:
                return (pybuf.address % self.recommended) == 0
            # minimum
            elif (pybuf.address % self.minimum) == 0:
                if self.size_within == 0:
                    return True
                else:
                    address = pybuf.address % self.size_within
                    return (address + self.width) <= self.size_within
            # no support
            else:
                return False

    def is_valid_recommended(self, buffer) -> bool:
        return self.is_valid(buffer, using_recommended=True)

    def is_valid_minimum(self, buffer) -> bool:
        return self.is_valid(buffer, using_recommended=False)
