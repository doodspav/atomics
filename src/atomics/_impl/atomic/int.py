from .base import Atomic, AtomicView, AtomicViewContext
from .core import AtomicCore

from .mixins.intops import IntegralOperationsMixin
from .mixins.properties import IntegralPropertiesMixin


class AtomicInt(Atomic, IntegralOperationsMixin, IntegralPropertiesMixin):

    def __init__(self, *, width: int):
        super().__init__(width=width, is_integral=True, is_signed=True)


class AtomicIntView(AtomicView, IntegralOperationsMixin, IntegralPropertiesMixin):

    def __init__(self, core: AtomicCore):
        super().__init__(core)


class AtomicIntViewContext(AtomicViewContext):

    def __init__(self, *, buffer):
        super().__init__(buffer=buffer, is_integral=True, is_signed=True)

    def __enter__(self) -> AtomicIntView:
        self._assert_enter_preconditions()
        self._entered = True
        return AtomicIntView(self._core)


class AtomicUint(Atomic, IntegralOperationsMixin, IntegralPropertiesMixin):

    def __init__(self, *, width: int):
        super().__init__(width=width, is_integral=True, is_signed=False)


class AtomicUintView(AtomicView, IntegralOperationsMixin, IntegralPropertiesMixin):

    def __init__(self, core: AtomicCore):
        super().__init__(core)


class AtomicUintViewContext(AtomicViewContext):

    def __init__(self, *, buffer):
        super().__init__(buffer=buffer, is_integral=True, is_signed=False)

    def __enter__(self) -> AtomicUintView:
        self._assert_enter_preconditions()
        self._entered = True
        return AtomicUintView(self._core)
