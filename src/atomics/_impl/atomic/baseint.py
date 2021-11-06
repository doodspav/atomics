from .base import Atomic, AtomicView, AtomicViewContext
from .core import AtomicCore

from .mixins.types import INTEGRAL


class AtomicIntegral(Atomic, INTEGRAL):

    def __init__(self, *, width: int, is_signed: bool):
        super().__init__(width=width, is_integral=True, is_signed=is_signed)


class AtomicIntegralView(AtomicView, INTEGRAL):

    def __init__(self, core: AtomicCore):
        super().__init__(core)


class AtomicIntegralViewContext(AtomicViewContext):

    def __init__(self, *, buffer, is_signed: bool):
        super().__init__(buffer=buffer, is_integral=True, is_signed=is_signed)

    def __enter__(self)-> AtomicIntegralView:
        self._assert_enter_preconditions()
        self._entered = True
        return AtomicIntegralView(self._core)
