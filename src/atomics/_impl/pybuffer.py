from .decorators import unreleased

import cffi


ffi = cffi.FFI()


class PyBuffer:

    def __init__(self, exporter, *, writeable: bool, force: bool = False):
        # check if __init__ has been called
        if hasattr(self, "_buf"):
            raise ValueError("PyBuffer object cannot be re-initialised.")
        # check if writeable can be satisfied
        view = memoryview(exporter)
        if writeable and view.readonly and not force:
            raise RuntimeError("Cannot create writeable PyBuffer from readonly exporter.")
        # get and save buffer
        self._buf = ffi.from_buffer("char[]", exporter, not view.readonly)
        self._obj = exporter
        self._len = view.nbytes
        self._readonly = not writeable

    @unreleased
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def __del__(self):
        self.release()

    def __bool__(self):
        return not self._released

    def __str__(self):
        if self:
            return f"{self.__class__.__name__}(address={self.address}, width={self.width}" \
                   f", readonly={self.readonly}, obj={self.obj})"
        else:
            return f"{self.__class__.__name__}(released)"

    def release(self) -> None:
        # this may be called in __del__ if exception is raised in __init__
        # we cannot rely on any attributes existing
        if hasattr(self, "_buf") and self._buf is not None:
            # if _buf exists, we can be confident the rest of the attributes do too
            ffi.release(self._buf)
            self._buf = None
            self._obj = None
            self._len = None
            self._readonly = None

    @property
    def _released(self) -> bool:
        return self._buf is not None

    @property
    @unreleased
    def address(self) -> int:
        return int(ffi.cast("uintptr_t", self._buf))

    @property
    @unreleased
    def width(self) -> int:
        return self._len

    @property
    @unreleased
    def readonly(self) -> bool:
        return self._readonly

    @property
    @unreleased
    def obj(self):
        return self._obj
