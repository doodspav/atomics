from ...enums import OpType

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

    @property
    def ops_supported(self) -> [OpType]:
        return self._core.ops_supported

    def __str__(self):
        msg = f"{self.__class__.__name__}(width={self.width}, " \
              f"readonly={self.readonly})"
        return msg


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
              f"width={self.width}, readonly={self.readonly}, " \
              f"signed={self.signed})"
        return msg

    def __int__(self):
        return self.load()

    @property
    def signed(self) -> bool:
        return self._core.signed
