cdef extern from "<patomic/types/memory_order.h>" nogil:

    # MEMORY ORDERS

    ctypedef enum patomic_memory_order_t:
        patomic_RELAXED
        patomic_CONSUME
        patomic_ACQUIRE
        patomic_RELEASE
        patomic_ACQ_REL
        patomic_SEQ_CST

    int patomic_is_valid_order(int order)
    int patomic_is_valid_store_order(int order)
    int patomic_is_valid_load_order(int order)

    int patomic_is_valid_fail_order(int succ, int fail)

    int patomic_cmpxchg_fail_order(int succ)
