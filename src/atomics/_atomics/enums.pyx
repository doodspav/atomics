from .patomic.types.memory_order cimport *

from .enums cimport *

import enum
import deprecation


cdef class _MemoryOrder:

    # cdef readonly int value

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


cdef class _OpType:

    # cdef readonly unsigned long value

    @staticmethod
    def _as_bin(value: int, fixed: bool = True) -> str:
        count = _optype_HIGHEST_BIT_POSITION + 2  # for 0b characters
        val_bin = format(value, f"#0{count}b") if fixed else bin(value)
        for i in range(len(val_bin) - 4, 2, -4):
            val_bin = val_bin[:i] + "'" + val_bin[i:]
        return val_bin

    def __cinit__(self, unsigned long value):
        cdef unsigned long offset = _optype_HIGHEST_BIT_POSITION
        cdef unsigned long extra_bits = (value >> offset) << offset;
        if extra_bits != 0:
            beb = _OpType._as_bin(extra_bits >> offset, fixed=False)
            raise ValueError(f"Remaining set bits {beb} << {offset} from value do not correspond to valid OpType.")
        self.value = value

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(value={_OpType._as_bin(self.value)})"


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
