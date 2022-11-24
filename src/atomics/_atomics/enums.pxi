from .patomic.types.memory_order cimport *

import enum
import deprecation


cdef class _MemoryOrder:

    cdef readonly int value

    def __cinit__(self, int value):
        if (value < patomic_RELAXED) or (value > patomic_SEQ_CST):
            raise ValueError(f"{value} is not a valid _MemoryOrder")
        self.value = value

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(value={self.value})"

    cpdef bint is_valid_store_order(self):
        return patomic_is_valid_store_order(self.value)

    cpdef bint is_valid_load_order(self):
        return patomic_is_valid_load_order(self.value)

    cpdef bint is_valid_fail_order_for(self, _MemoryOrder succ):
        return patomic_is_valid_fail_order(succ.value, self.value)


class MemoryOrder(enum.IntEnum):

    RELAXED = patomic_RELAXED
    CONSUME = patomic_ACQUIRE  # patomic_CONSUME would be useless in Python, it's already useless in C
    ACQUIRE = patomic_ACQUIRE
    RELEASE = patomic_RELEASE
    ACQ_REL = patomic_ACQ_REL
    SEQ_CST = patomic_SEQ_CST

    def __init__(self, value: int):
        self._cinfo = _MemoryOrder(value)

    def is_valid_store_order(self) -> bool:
        return self._cinfo.is_valid_store_order()

    def is_valid_load_order(self) -> bool:
        return self._cinfo.is_valid_load_order()

    def is_valid_fail_order_for(self, succ: "MemoryOrder") -> bool:
        return self._cinfo.is_valid_fail_order_for(succ._cinfo)

    @deprecation.deprecated(details="Use is_valid_fail_order_for instead.")
    def is_valid_fail_order(self, succ: "MemoryOrder") -> bool:
        return self._cinfo.is_valid_fail_order_for(succ._cinfo)
