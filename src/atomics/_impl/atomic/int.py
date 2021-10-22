from .baseint import AtomicIntegralBase


class AtomicSInt(AtomicIntegralBase):

    def __init__(self, buffer_or_width):
        super().__init__(buffer_or_width, is_signed=True)


class AtomicUInt(AtomicIntegralBase):

    def __init__(self, buffer_or_width):
        super().__init__(buffer_or_width, is_signed=False)
