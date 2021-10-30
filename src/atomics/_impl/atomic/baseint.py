from .base import AtomicBase, AtomicViewBase


class AtomicIntegralBase(AtomicBase):

    def __init__(self, *, width: int, is_signed: bool):
        super().__init__(width=width, is_integral=True, is_signed=is_signed)

    @property
    def signed(self) -> bool:
        return self._is_signed


class AtomicIntegralViewBase(AtomicViewBase):

    def __init__(self, *, buffer, is_signed: bool):
        super().__init__(buffer=buffer, is_integral=True, is_signed=is_signed)

    @property
    def signed(self) -> bool:
        return self._is_signed
