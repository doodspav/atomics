from .mixins.properties import PropertiesMixin
from .mixins.supported import SupportedMixin

from ..alignment import Alignment
from ..exceptions import AlignmentError, UnsupportedWidthException
from ..patomic import Patomic
from ..pybuffer import PyBuffer


class AtomicBase(PropertiesMixin, SupportedMixin):

    def __init__(self, *, width: int, is_integral: bool, is_signed: bool):
        # check if object has been initialised
        if hasattr(self, "_buffer"):
            raise ValueError("Atomic object cannot be re-initialised.")
        self._is_integral: bool = is_integral
        self._is_signed: bool = is_signed
        # check type
        if not isinstance(width, int):
            raise TypeError("Keyword argument 'width' must have type 'int'.")
        # create buffer
        self._buffer = PyBuffer(bytearray(width), writeable=True)
        # check ops are available
        p = Patomic()
        self._ops = p.ops(width)
        if p.count_nonnull_ops(self._ops, readonly=False) == 0:
            raise UnsupportedWidthException(width, readonly=False)
        # check alignment
        align = Alignment(width)
        if not align.is_valid_recommended(self._buffer.obj):
            raise AlignmentError(width, self._buffer.address, using_recommended=True)
        # init SupportedMixin to get _supported and ops_supported()
        super().__init__()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def __del__(self):
        self.release()

    def release(self) -> None:
        if hasattr(self, "_buffer"):
            self._buffer.release()


class AtomicViewBase(PropertiesMixin, SupportedMixin):

    def __init__(self, *, buffer, is_integral: bool, is_signed: bool):
        # check if object has been initialised
        if hasattr(self, "_buffer"):
            raise ValueError("AtomicView object cannot be re-initialised.")
        self._is_integral: bool = is_integral
        self._is_signed: bool = is_signed
        self._enter_called: bool = False
        self._exit_called: bool = False
        # check and deal with buffer
        try:
            with memoryview(buffer) as view:
                self._buffer = PyBuffer(buffer, writeable=(not view.readonly))
        except TypeError:
            pass
        # check for TypeError; raise outside exception handler for nicer error message
        if not hasattr(self, "_buffer"):
            em = "Keyword argument 'buffer' must support the buffer protocol."
            raise TypeError(em)
        # check ops are available
        p = Patomic()
        self._ops = p.ops(self.width)
        if p.count_nonnull_ops(self._ops, readonly=self.readonly) == 0:
            raise UnsupportedWidthException(self.width, readonly=self.readonly)
        # check alignment
        align = Alignment(self.width)
        if not align.is_valid_recommended(self._buffer.obj):
            raise AlignmentError(self.width, self._buffer.address, using_recommended=True)
        # init SupportedMixin to get _supported and ops_supported()
        super().__init__()

    def __enter__(self):
        self._enter_called = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._exit_called = True
        self.release()

    def __del__(self):
        self.release()

    def release(self) -> None:
        if hasattr(self, "_buffer"):
            self._buffer.release()

    @property
    def _address(self) -> int:
        # make sure we can't use this outside of context-manager
        if self._exit_called or not self._enter_called:
            raise RuntimeError("Operation cannot be called outside a context manager.")
        else:
            return self._buffer.address
