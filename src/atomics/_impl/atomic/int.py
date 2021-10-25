from .baseint import AtomicIntegralBase


class AtomicInt(AtomicIntegralBase):

    def __init__(self, *, buffer_or_width):
        super().__init__(buffer_or_width, is_signed=True)

    @classmethod
    def from_buffer(cls, buffer):
        return cls(buffer_or_width=buffer)

    @classmethod
    def from_width(cls, width: int):
        return cls(buffer_or_width=width)


class AtomicUint(AtomicIntegralBase):

    def __init__(self, *, buffer_or_width):
        super().__init__(buffer_or_width, is_signed=False)

    @classmethod
    def from_buffer(cls, buffer):
        return cls(buffer_or_width=buffer)

    @classmethod
    def from_width(cls, width: int):
        return cls(buffer_or_width=width)
