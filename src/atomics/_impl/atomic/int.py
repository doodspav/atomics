from .baseint import AtomicIntegralBase, AtomicIntegralViewBase
from .mixins.intops import IntegralOperationsMixin


class AtomicInt(AtomicIntegralBase, IntegralOperationsMixin):

    def __init__(self, *, width: int):
        super().__init__(width=width, is_signed=True)


class AtomicUint(AtomicIntegralBase, IntegralOperationsMixin):

    def __init__(self, *, width: int):
        super().__init__(width=width, is_signed=False)


class AtomicIntView(AtomicIntegralViewBase, IntegralOperationsMixin):

    def __init__(self, *, buffer):
        super().__init__(buffer=buffer, is_signed=True)


class AtomicUintView(AtomicIntegralViewBase, IntegralOperationsMixin):

    def __init__(self, *, buffer):
        super().__init__(buffer=buffer, is_signed=True)
