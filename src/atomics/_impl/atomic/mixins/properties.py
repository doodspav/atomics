from ..core import AtomicCore

from typing import Callable


class BasePropertiesMixin:

    _core: AtomicCore

    @property
    def _address(self) -> int:
        return self._core.address

    @property
    def width(self) -> int:
        return self._core.width

    @property
    def readonly(self) -> bool:
        return self._core.readonly


class BytePropertiesMixin(BasePropertiesMixin):

    load: Callable[[], bytes]

    def __str__(self):
        msg = f"{self.__class__.__name__}(value={self.load()}, " \
              f"width={self.width}, readonly={self.readonly})"
        return msg

    def __bytes__(self):
        return self.load()


class IntegralPropertiesMixin(BasePropertiesMixin):

    load: Callable[[], int]

    def __str__(self):
        msg = f"{self.__class__.__name__}(value={self.load()}, " \
              f"width={self.width}, readonly={self.readonly})"
        return msg

    def __int__(self):
        return self.load()

    @property
    def signed(self) -> bool:
        return self._core.signed
