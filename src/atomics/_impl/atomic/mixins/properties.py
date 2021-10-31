from ...pybuffer import PyBuffer


class PropertiesMixin:

    _buffer: PyBuffer

    @property
    def _address(self) -> int:
        return self._buffer.address

    @property
    def width(self) -> int:
        return len(self._buffer)

    @property
    def readonly(self) -> bool:
        return self._buffer.readonly
