from ..alignment import Alignment
from ..exceptions import AlignmentError, UnsupportedWidthException
from ..patomic import Patomic
from ..pybuffer import PyBuffer

from .core import AtomicCore


class AtomicBase:

    def __init__(self, *, width: int, is_integral: bool, is_signed: bool):
        # check if object has been initialised
        if hasattr(self, "_core"):
            raise ValueError("Atomic object cannot be re-initialised.")
        # check type
        if not isinstance(width, int):
            raise TypeError("Keyword argument 'width' must have type 'int'.")
        # check ops are available
        p = Patomic()
        ops = p.ops(width)
        if p.count_nonnull_ops(ops, readonly=False) == 0:
            raise UnsupportedWidthException(width, readonly=False)
        # check alignment of buffer
        pybuf = PyBuffer(bytearray(width), writeable=True)
        align = Alignment(width)
        if not align.is_valid_recommended(pybuf.obj):
            raise AlignmentError(width, pybuf.address, using_recommended=True)
        # create core
        self._core = AtomicCore(pybuf, ops, is_integral=is_integral, is_signed=is_signed)

    def __del__(self):
        if hasattr(self, "_core"):
            self._core.release()


class AtomicViewBase:

    def __init__(self, core: AtomicCore):
        # check if object has been initialised
        if hasattr(self, "_core"):
            raise ValueError("AtomicView object cannot be re-initialised.")
        # check type
        if not isinstance(core, AtomicCore):
            raise TypeError("Positional argument 'core' must have type 'AtomicCore'.")
        # store core
        self._core = core

    def __del__(self):
        if hasattr(self, "_core"):
            self._core.release()


class AtomicViewBaseContext:

    def __init__(self, *, buffer, is_integral: bool, is_signed: bool):
        # check if object has been initialised
        if hasattr(self, "_core"):
            raise ValueError("AtomicViewContext object cannot be re-initialised.")
        # check and deal with buffer
        pybuf = None
        try:
            with memoryview(buffer) as view:
                pybuf = PyBuffer(buffer, writeable=(not view.readonly))
        except TypeError:
            pass
        # check for TypeError; raise outside exception handler for nicer error message
        if pybuf is None:
            em = "Keyword argument 'buffer' must support the buffer protocol."
            raise TypeError(em)
        # check ops are available
        p = Patomic()
        ops = p.ops(pybuf.width)
        if p.count_nonnull_ops(ops, readonly=pybuf.readonly) == 0:
            # pybuf MUST be released before function exit
            width, ro = pybuf.width, pybuf.readonly
            pybuf.release()
            raise UnsupportedWidthException(width, readonly=ro)
        # check alignment of buffer
        align = Alignment(pybuf.width)
        if not align.is_valid_recommended(pybuf.obj):
            # pybuf MUST be released before function exit
            width, addr = pybuf.width, pybuf.address
            pybuf.release()
            raise AlignmentError(width, addr, using_recommended=True)
        # create core
        self._core = AtomicCore(pybuf, ops, is_integral=is_integral, is_signed=is_signed)
        self._entered = False
        self._exited = False

    def __enter__(self) -> AtomicViewBase:
        self._assert_enter_preconditions()
        self._entered = True
        return AtomicViewBase(self._core)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._exited = True
        self.release()

    def __del__(self):
        self.release()

    def release(self) -> None:
        if hasattr(self, "_core"):
            if self._entered and not self._exited:
                raise ValueError("Cannot call 'release' while context is open.")
            else:
                self._core.release()

    def _assert_enter_preconditions(self) -> None:
        if self._entered:
            raise ValueError("Cannot open context multiple times.")
        elif not self._core:
            raise ValueError("Cannot open context after calling 'release'.")
