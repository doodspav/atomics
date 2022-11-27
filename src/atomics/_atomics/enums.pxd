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
    /* extra */
    static const unsigned long _optype_HIGHEST_BIT_POSITION = 27ul;
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
    # extra
    const unsigned long _optype_HIGHEST_BIT_POSITION


cdef class _MemoryOrder:

    cdef readonly int value

    # def __cinit__(self, int value)
    # def __repr__(self) -> str

    cpdef bint is_valid_store_order(self)
    cpdef bint is_valid_load_order(self)
    cpdef bint is_valid_fail_order_for(self, _MemoryOrder succ)


cdef class _OpType:

    cdef readonly unsigned long value

    # @staticmethod
    # def _as_bin(value: int, fixed: bool = True) -> str:
    # def __cinit__(self, unsigned long value)
    # def __repr__(self) -> str
