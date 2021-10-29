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

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def __del__(self):
        self.release()

    def __len__(self) -> int:
        if self._len is not None:
            return self._len
        else:
            raise ValueError("Operation forbidden on released PyBuffer object.")

    def release(self) -> None:
        if hasattr(self, "_buf") and self._buf is not None:
            ffi.release(self._buf)
            self._buf = None
            self._obj = None
            self._len = None
            self._readonly = None

    @property
    def address(self) -> int:
        if self._buf is not None:
            return int(ffi.cast("uintptr_t", self._buf))
        else:
            raise ValueError("Operation forbidden on released PyBuffer object.")

    @property
    def readonly(self) -> bool:
        if self._readonly is not None:
            return self._readonly
        else:
            raise ValueError("Operation forbidden on released PyBuffer object.")

    @property
    def obj(self):
        if self._obj is not None:
            return self._obj
        else:
            raise ValueError("Operation forbidden on released PyBuffer object.")
