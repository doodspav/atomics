import enum

from atomics._atomics.patomic cimport *


cdef class _CEnumBase:

    cdef int c_value

    def __cinit__(self, value):
        self.c_value = value


class MemoryOrder(_CEnumBase, enum.Enum):

    RELAXED = patomic_RELAXED
    # CONSUME = patomic_CONSUME
    ACQUIRE = patomic_ACQUIRE
    RELEASE = patomic_RELEASE
    ACQ_REL = patomic_ACQ_REL
    SEQ_CST = patomic_SEQ_CST

    def __init__(self, value):
        self.value = value


cdef c_get_value(order: MemoryOrder):
    return order.c_value

cpdef get_value(order: MemoryOrder):
    return c_get_value(order)
