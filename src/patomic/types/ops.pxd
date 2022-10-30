from transaction cimport *


cdef extern from "<patomic/types/ops.h>":

    # IMPLICIT FUNCTIONS

    ctypedef void (* patomic_opsig_store_t) (void *obj, const void *desired)
    ctypedef void (* patomic_opsig_load_t) (const void *obj, void *ret)

    ctypedef void (* patomic_opsig_exchange_t) (void *obj, const void *desired, void *ret)
    ctypedef int  (* patomic_opsig_cmpxchg_t) (void *obj, void *expected, const void *desired)

    ctypedef int (* patomic_opsig_test_t) (const void *obj, int offset)
    ctypedef int (* patomic_opsig_test_modify_t) (void *obj, int offset)

    ctypedef void (* patomic_opsig_fetch_t) (void *obj, const void *arg, void *ret)
    ctypedef void (* patomic_opsig_fetch_noarg_t) (void *obj, void *ret)

    ctypedef void (* patomic_opsig_void_t) (void *obj, const void *arg)
    ctypedef void (* patomic_opsig_void_noarg_t) (void *obj);

    # IMPLICIT STRUCTS

    ctypedef struct patomic_ops_arithmetic_t:
        # in place
        patomic_opsig_void_t fp_add
        patomic_opsig_void_t fp_sub
        patomic_opsig_void_noarg_t fp_inc
        patomic_opsig_void_noarg_t fp_dec
        patomic_opsig_void_noarg_t fp_neg
        # fetch
        patomic_opsig_fetch_t fp_fetch_add
        patomic_opsig_fetch_t fp_fetch_sub
        patomic_opsig_fetch_noarg_t fp_fetch_inc
        patomic_opsig_fetch_noarg_t fp_fetch_dec
        patomic_opsig_fetch_noarg_t fp_fetch_neg

    ctypedef struct patomic_ops_binary_t:
        # in place
        patomic_opsig_void_t fp_or
        patomic_opsig_void_t fp_xor
        patomic_opsig_void_t fp_and
        patomic_opsig_void_noarg_t fp_not
        # fetch
        patomic_opsig_fetch_t fp_fetch_or
        patomic_opsig_fetch_t fp_fetch_xor
        patomic_opsig_fetch_t fp_fetch_and
        patomic_opsig_fetch_noarg_t fp_fetch_not

    ctypedef struct patomic_ops_bitwise_t:
        patomic_opsig_test_t fp_test
        patomic_opsig_test_modify_t fp_test_compl
        patomic_opsig_test_modify_t fp_test_set
        patomic_opsig_test_modify_t fp_test_reset

    ctypedef struct patomic_ops_xchg_t:
        patomic_opsig_exchange_t fp_exchange
        patomic_opsig_cmpxchg_t fp_cmpxchg_weak
        patomic_opsig_cmpxchg_t fp_cmpxchg_strong

    ctypedef struct patomic_ops_t:
        patomic_opsig_store_t fp_store
        patomic_opsig_load_t fp_load
        patomic_ops_xchg_t xchg_ops
        patomic_ops_bitwise_t bitwise_ops
        patomic_ops_binary_t binary_ops
        patomic_ops_arithmetic_t signed_ops
        patomic_ops_arithmetic_t unsigned_ops

    # EXPLICIT FUNCTIONS

    ctypedef void (* patomic_opsig_explicit_store_t) (void *obj, const void *desired, int order)
    ctypedef void (* patomic_opsig_explicit_load_t) (const void *obj, int order, void *ret)

    ctypedef void (* patomic_opsig_explicit_exchange_t) (void *obj, const void *desired, int order, void *ret)
    ctypedef int  (* patomic_opsig_explicit_cmpxchg_t) (void *obj, void *expected, const void *desired, int succ, int fail)

    ctypedef int (* patomic_opsig_explicit_test_t) (const void *obj, int offset, int order)
    ctypedef int (* patomic_opsig_explicit_test_modify_t) (void *obj, int offset, int order)

    ctypedef void (* patomic_opsig_explicit_fetch_t) (void *obj, const void *arg, int order, void *ret)
    ctypedef void (* patomic_opsig_explicit_fetch_noarg_t) (void *obj, int order, void *ret)

    ctypedef void (* patomic_opsig_explicit_void_t) (void *obj, const void *arg, int order)
    ctypedef void (* patomic_opsig_explicit_void_noarg_t) (void *obj, int order)

    # EXPLICIT STRUCTS

    ctypedef struct patomic_ops_explicit_arithmetic_t:
        # in place
        patomic_opsig_explicit_void_t fp_add
        patomic_opsig_explicit_void_t fp_sub
        patomic_opsig_explicit_void_noarg_t fp_inc
        patomic_opsig_explicit_void_noarg_t fp_dec
        patomic_opsig_explicit_void_noarg_t fp_neg
        # fetch
        patomic_opsig_explicit_fetch_t fp_fetch_add
        patomic_opsig_explicit_fetch_t fp_fetch_sub
        patomic_opsig_explicit_fetch_noarg_t fp_fetch_inc
        patomic_opsig_explicit_fetch_noarg_t fp_fetch_dec
        patomic_opsig_explicit_fetch_noarg_t fp_fetch_neg

    ctypedef struct patomic_ops_explicit_binary_t:
        # in place
        patomic_opsig_explicit_void_t fp_or
        patomic_opsig_explicit_void_t fp_xor
        patomic_opsig_explicit_void_t fp_and
        patomic_opsig_explicit_void_noarg_t fp_not
        # fetch
        patomic_opsig_explicit_fetch_t fp_fetch_or
        patomic_opsig_explicit_fetch_t fp_fetch_xor
        patomic_opsig_explicit_fetch_t fp_fetch_and
        patomic_opsig_explicit_fetch_noarg_t fp_fetch_not

    ctypedef struct patomic_ops_explicit_bitwise_t:
        patomic_opsig_explicit_test_t fp_test
        patomic_opsig_explicit_test_modify_t fp_test_compl
        patomic_opsig_explicit_test_modify_t fp_test_set
        patomic_opsig_explicit_test_modify_t fp_test_reset

    ctypedef struct patomic_ops_explicit_xchg_t:
        patomic_opsig_explicit_exchange_t fp_exchange
        patomic_opsig_explicit_cmpxchg_t fp_cmpxchg_weak
        patomic_opsig_explicit_cmpxchg_t fp_cmpxchg_strong

    ctypedef struct patomic_ops_explicit_t:
        patomic_opsig_explicit_store_t fp_store
        patomic_opsig_explicit_load_t fp_load
        patomic_ops_explicit_xchg_t xchg_ops
        patomic_ops_explicit_bitwise_t bitwise_ops
        patomic_ops_explicit_binary_t binary_ops
        patomic_ops_explicit_arithmetic_t signed_ops
        patomic_ops_explicit_arithmetic_t unsigned_ops
