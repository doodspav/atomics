from .baseint import AtomicIntegral, AtomicIntegralView, AtomicIntegralViewContext
from .core import AtomicCore


class AtomicInt(AtomicIntegral):

    def __init__(self, *, width: int):
        super().__init__(width=width, is_signed=True)


class AtomicIntView(AtomicIntegralView):

    def __init__(self, core: AtomicCore):
        super().__init__(core)


class AtomicIntViewContext(AtomicIntegralViewContext):

    def __init__(self, *, buffer):
        super().__init__(buffer=buffer, is_signed=True)

    def __enter__(self) -> AtomicIntView:
        self._assert_enter_preconditions()
        self._entered = True
        return AtomicIntView(self._core)


class AtomicUint(AtomicIntegral):

    def __init__(self, *, width: int):
        super().__init__(width=width, is_signed=False)


class AtomicUintView(AtomicIntegralView):

    def __init__(self, core: AtomicCore):
        super().__init__(core)


class AtomicUintViewContext(AtomicIntegralViewContext):

    def __init__(self, *, buffer):
        super().__init__(buffer=buffer, is_signed=False)

    def __enter__(self) -> AtomicUintView:
        self._assert_enter_preconditions()
        self._entered = True
        return AtomicUintView(self._core)
