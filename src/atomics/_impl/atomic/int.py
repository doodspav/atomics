from .base import AtomicBase, AtomicViewBase, AtomicViewBaseContext
from .core import AtomicCore

from .mixins.intops import IntegralOperationsMixin
from .mixins.properties import IntegralPropertiesMixin


class AtomicInt(AtomicBase, IntegralOperationsMixin, IntegralPropertiesMixin):

    def __init__(self, *, width: int):
        super().__init__(width=width, is_integral=True, is_signed=True)


class AtomicIntView(AtomicViewBase, IntegralOperationsMixin, IntegralPropertiesMixin):

    def __init__(self, core: AtomicCore):
        super().__init__(core)


class AtomicIntViewContext(AtomicViewBaseContext):

    def __init__(self, *, buffer):
        super().__init__(buffer=buffer, is_integral=True, is_signed=True)

    def __enter__(self) -> AtomicIntView:
        self._assert_enter_preconditions()
        self._entered = True
        return AtomicIntView(self._core)


class AtomicUint(AtomicBase, IntegralOperationsMixin, IntegralPropertiesMixin):

    def __init__(self, *, width: int):
        super().__init__(width=width, is_integral=True, is_signed=False)


class AtomicUintView(AtomicViewBase, IntegralOperationsMixin, IntegralPropertiesMixin):

    def __init__(self, core: AtomicCore):
        super().__init__(core)


class AtomicUintViewContext(AtomicViewBaseContext):

    def __init__(self, *, buffer):
        super().__init__(buffer=buffer, is_integral=True, is_signed=False)

    def __enter__(self) -> AtomicUintView:
        self._assert_enter_preconditions()
        self._entered = True
        return AtomicUintView(self._core)
