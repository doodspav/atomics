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


# this is required because we want these to be compile-time constants that can be optimised by the compiler
# we can't use an enum because int might only be 16 bits
# technically const doesn't create a compile-time constant, but your compiler can probably optimise it into one
cdef extern from * nogil:
    """
    /* ldst */
    static const unsigned long _optype_LOAD  = 1ul << 0ul;
    static const unsigned long _optype_STORE = 1ul << 1ul;
    /* xchg */
    static const unsigned long _optype_EXCHANGE       = 1ul << 2ul;
    static const unsigned long _optype_CMPXCHG_WEAK   = 1ul << 3ul;
    static const unsigned long _optype_CMPXCHG_STRONG = 1ul << 4ul;
    /* bit */
    static const unsigned long _optype_BIT_TEST       = 1ul << 5ul;
    static const unsigned long _optype_BIT_TEST_COMPL = 1ul << 6ul;
    static const unsigned long _optype_BIT_TEST_SET   = 1ul << 7ul;
    static const unsigned long _optype_BIT_TEST_RESET = 1ul << 8ul;
    /* binary */
    static const unsigned long _optype_OR  = 1ul << 9ul;
    static const unsigned long _optype_XOR = 1ul << 10ul;
    static const unsigned long _optype_AND = 1ul << 11ul;
    static const unsigned long _optype_NOT = 1ul << 12ul;
    /* binary fetch */
    static const unsigned long _optype_FETCH_OR  = 1ul << 13ul;
    static const unsigned long _optype_FETCH_XOR = 1ul << 14ul;
    static const unsigned long _optype_FETCH_AND = 1ul << 15ul;
    static const unsigned long _optype_FETCH_NOT = 1ul << 16ul;
    /* arithmetic */
    static const unsigned long _optype_ADD = 1ul << 17ul;
    static const unsigned long _optype_SUB = 1ul << 18ul;
    static const unsigned long _optype_INC = 1ul << 19ul;
    static const unsigned long _optype_DEC = 1ul << 20ul;
    static const unsigned long _optype_NEG = 1ul << 21ul;
    /* arithmetic fetch */
    static const unsigned long _optype_FETCH_ADD = 1ul << 22ul;
    static const unsigned long _optype_FETCH_SUB = 1ul << 23ul;
    static const unsigned long _optype_FETCH_INC = 1ul << 24ul;
    static const unsigned long _optype_FETCH_DEC = 1ul << 25ul;
    static const unsigned long _optype_FETCH_NEG = 1ul << 26ul;
    """
    # ldst
    const unsigned long _optype_LOAD
    const unsigned long _optype_STORE
    # xchg
    const unsigned long _optype_EXCHANGE
    const unsigned long _optype_CMPXCHG_WEAK
    const unsigned long _optype_CMPXCHG_STRONG
    # bit
    const unsigned long _optype_BIT_TEST
    const unsigned long _optype_BIT_TEST_COMPL
    const unsigned long _optype_BIT_TEST_SET
    const unsigned long _optype_BIT_TEST_RESET
    # binary
    const unsigned long _optype_OR
    const unsigned long _optype_XOR
    const unsigned long _optype_AND
    const unsigned long _optype_NOT
    # binary fetch
    const unsigned long _optype_FETCH_OR
    const unsigned long _optype_FETCH_XOR
    const unsigned long _optype_FETCH_AND
    const unsigned long _optype_FETCH_NOT
    # arithmetic
    const unsigned long _optype_ADD
    const unsigned long _optype_SUB
    const unsigned long _optype_INC
    const unsigned long _optype_DEC
    const unsigned long _optype_NEG
    # arithmetic fetch
    const unsigned long _optype_FETCH_ADD
    const unsigned long _optype_FETCH_SUB
    const unsigned long _optype_FETCH_INC
    const unsigned long _optype_FETCH_DEC
    const unsigned long _optype_FETCH_NEG


cdef class _OpType:

    cdef readonly unsigned long value

    def __cinit__(self, unsigned long value):
        self.value = value

    def __repr__(self) -> str:
        val_bin = format(self.value, "#029b")  # 29 because number of bits (27) + 2
        for i in range(len(val_bin) - 4, 2, -4):
            val_bin = val_bin[:i] + "'" + val_bin[i:]
        return f"{self.__class__.__qualname__}(value={val_bin})"


class OpType(enum.Flag):

    # none
    NONE = 0
    # ldst
    LOAD  = _optype_LOAD
    STORE = _optype_STORE
    # xchg
    EXCHANGE       = _optype_EXCHANGE
    CMPXCHG_WEAK   = _optype_CMPXCHG_WEAK
    CMPXCHG_STRONG = _optype_CMPXCHG_STRONG
    # bit
    BIT_TEST       = _optype_BIT_TEST
    BIT_TEST_COMPL = _optype_BIT_TEST_COMPL
    BIT_TEST_SET   = _optype_BIT_TEST_SET
    BIT_TEST_RESET = _optype_BIT_TEST_RESET
    # binary
    OR  = _optype_OR
    XOR = _optype_XOR
    AND = _optype_AND
    NOT = _optype_NOT
    # binary fetch
    FETCH_OR  = _optype_FETCH_OR
    FETCH_XOR = _optype_FETCH_XOR
    FETCH_AND = _optype_FETCH_AND
    FETCH_NOT = _optype_FETCH_NOT
    # arithmetic
    ADD = _optype_ADD
    SUB = _optype_SUB
    INC = _optype_INC
    DEC = _optype_DEC
    NEG = _optype_NEG
    # arithmetic fetch
    FETCH_ADD = _optype_FETCH_ADD
    FETCH_SUB = _optype_FETCH_SUB
    FETCH_INC = _optype_FETCH_INC
    FETCH_DEC = _optype_FETCH_DEC
    FETCH_NEG = _optype_FETCH_NEG
    # grouped
    LDST  = LOAD | STORE
    XCHG  = EXCHANGE | CMPXCHG_WEAK | CMPXCHG_STRONG
    BIT   = BIT_TEST | BIT_TEST_COMPL | BIT_TEST_SET | BIT_TEST_RESET
    BIN_V = OR | XOR | AND | NOT
    BIN_F = FETCH_OR | FETCH_XOR | FETCH_AND | FETCH_NOT
    BIN   = BIN_V | BIN_F
    ARI_V = ADD | SUB | INC | DEC | NEG
    ARI_F = FETCH_ADD | FETCH_SUB | FETCH_INC | FETCH_DEC | FETCH_NEG
    ARI   = ARI_V | ARI_F
    # all
    ALL = LDST | XCHG | BIT | BIN | ARI

    def __init__(self, value: int):
        self._cinfo = _OpType(value)
