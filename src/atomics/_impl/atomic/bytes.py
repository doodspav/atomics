from .base import AtomicBase, AtomicViewBase, AtomicViewBaseContext
from .core import AtomicCore

from .mixins.byteops import ByteOperationsMixin
from .mixins.properties import BytePropertiesMixin


class AtomicBytes(AtomicBase, ByteOperationsMixin, BytePropertiesMixin):

    def __init__(self, *, width: int):
        super().__init__(width=width, is_integral=False, is_signed=False)


class AtomicBytesView(AtomicViewBase, ByteOperationsMixin, BytePropertiesMixin):

    def __init__(self, core: AtomicCore):
        super().__init__(core)


class AtomicBytesViewContext(AtomicViewBaseContext):

    def __init__(self, *, buffer):
        super().__init__(buffer=buffer, is_integral=False, is_signed=False)

    def __enter__(self) -> AtomicBytesView:
        self._assert_enter_preconditions()
        self._entered = True
        return AtomicBytesView(self._core)
