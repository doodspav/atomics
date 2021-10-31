from .base import AtomicBase, AtomicViewBase
from .mixins.byteops import ByteOperationsMixin


class AtomicBytes(AtomicBase, ByteOperationsMixin):

    def __init__(self, *, width: int):
        super().__init__(width=width, is_integral=False, is_signed=False)


class AtomicBytesView(AtomicViewBase, ByteOperationsMixin):

    def __init__(self, *, buffer):
        super().__init__(buffer=buffer, is_integral=False, is_signed=False)
