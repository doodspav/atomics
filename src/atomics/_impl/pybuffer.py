import cffi


class PyBuffer:

    def __init__(self, exporter, *, writeable: bool, force: bool = False):
        # check if __init__ has been called
        if hasattr(self, "_ffi"):
            raise ValueError("PyBuffer object can only be initialised once.")
        # check if writeable can be satisfied
        view = memoryview(exporter)
        if writeable and view.readonly and not force:
            raise RuntimeError("Cannot create writeable PyBuffer from readonly exporter.")
        # get and save buffer
        self._ffi = cffi.FFI()
        self._buf = self._ffi.from_buffer("char[]", exporter, not view.readonly)
        self._obj = exporter
        self._len = view.nbytes
        self._readonly = not writeable

    def __del__(self):
        self.release()

    def __len__(self) -> int:
        if self._ffi is not None:
            return self._len
        else:
            raise ValueError("Operation forbidden on released PyBuffer object.")

    def release(self) -> None:
        if self._ffi is not None:
            self._ffi.release(self._buf)
            self._ffi = None
            self._buf = None
            self._obj = None

    @property
    def address(self) -> int:
        if self._ffi is not None:
            return int(self._ffi.cast("uintptr_t", self._buf))
        else:
            raise ValueError("Operation forbidden on released PyBuffer object.")

    @property
    def readonly(self) -> bool:
        if self._ffi is not None:
            return self._readonly
        else:
            raise ValueError("Operation forbidden on released PyBuffer object.")

    @property
    def obj(self):
        if self._ffi is not None:
            return self._obj
        else:
            raise ValueError("Operation forbidden on released PyBuffer object.")
