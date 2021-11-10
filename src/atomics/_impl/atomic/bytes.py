from .base import Atomic, AtomicView, AtomicViewContext
from .core import AtomicCore

from .mixins.types import BYTES


class AtomicBytes(Atomic, BYTES):

    def __init__(self, *, width: int):
        super().__init__(width=width, is_integral=False, is_signed=False)


class AtomicBytesView(AtomicView, BYTES):

    def __init__(self, core: AtomicCore):
        super().__init__(core)


class AtomicBytesViewContext(AtomicViewContext):

    def __init__(self, *, buffer):
        super().__init__(buffer=buffer, is_integral=False, is_signed=False)

    def __enter__(self) -> AtomicBytesView:
        self._assert_enter_preconditions()
        self._entered = True
        return AtomicBytesView(self._core)
