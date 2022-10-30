from .transaction cimport *


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

    # TRANSACTION FUNCTIONS

    ctypedef void (* patomic_opsig_transaction_store_t) \
        (void *obj,
         const void *desired,
         patomic_transaction_config_t config,
         patomic_transaction_result_t *result)

    ctypedef void (* patomic_opsig_transaction_load_t) \
        (const void *obj,
         patomic_transaction_config_t config,
         void *ret,
         patomic_transaction_result_t *result)

    ctypedef void (* patomic_opsig_transaction_exchange_t) \
        (void *obj,
         const void *desired,
         patomic_transaction_config_t config,
         void *ret,
         patomic_transaction_result_t *result)

    ctypedef int (* patomic_opsig_transaction_cmpxchg_t) \
        (void *obj,
         void *expected,
         const void *desired,
         patomic_transaction_config_wfb_t config,
         patomic_transaction_result_wfb_t *result)

    ctypedef int (* patomic_opsig_transaction_test_t) \
        (const void *obj,
         size_t offset,
         patomic_transaction_config_t config,
         patomic_transaction_result_t *result)

    ctypedef int (* patomic_opsig_transaction_test_modify_t) \
        (void *obj,
         size_t offset,
         patomic_transaction_config_t config,
         patomic_transaction_result_t *result)

    ctypedef void (* patomic_opsig_transaction_fetch_t) \
        (void *obj,
         const void *arg,
         patomic_transaction_config_t config,
         void *ret,
         patomic_transaction_result_t *result)

    ctypedef void (* patomic_opsig_transaction_fetch_noarg_t) \
        (void *obj,
         patomic_transaction_config_t config,
         void *ret,
         patomic_transaction_result_t *result)

    ctypedef void (* patomic_opsig_transaction_void_t) \
        (void *obj,
         const void *arg,
         patomic_transaction_config_t config,
         patomic_transaction_result_t *result)

    ctypedef void (* patomic_opsig_transaction_void_noarg_t) \
        (void *obj,
         patomic_transaction_config_t config,
         patomic_transaction_result_t *result)

    # TRANSACTION EXCLUSIVE FUNCTIONS

    ctypedef int (* patomic_opsig_transaction_double_cmpxchg_t) \
        (patomic_transaction_cmpxchg_t cxa,
         patomic_transaction_cmpxchg_t cxb,
         patomic_transaction_config_wfb_t config,
         patomic_transaction_result_wfb_t *result)

    ctypedef int (* patomic_opsig_transaction_multi_cmpxchg_t) \
        (const patomic_transaction_cmpxchg_t *cxs_buf,
         size_t cxs_len,
         patomic_transaction_config_wfb_t config,
         patomic_transaction_result_wfb_t *result)

    ctypedef void (* patomic_opsig_transaction_generic_t) \
        (void (* fn) (void *),
         void *ctx,
         patomic_transaction_config_t config,
         patomic_transaction_result_t *result)

    ctypedef int (* patomic_opsig_transaction_generic_wfb_t) \
        (void (* fn) (void *),
         void *ctx,
         void (* fallback_fn) (void *),
         void *fallback_ctx,
         patomic_transaction_config_wfb_t config,
         patomic_transaction_result_wfb_t *result)

    ctypedef int (* patomic_opsig_transaction_flag_test_t) (const patomic_transaction_flag_t *flag)
    ctypedef int (* patomic_opsig_transaction_flag_test_set_t) (patomic_transaction_flag_t *flag)
    ctypedef int (* patomic_opsig_transaction_flag_clear_t) (patomic_transaction_flag_t *flag)

    ctypedef unsigned int (* patomic_opsig_transaction_tbegin_t) ()
    ctypedef void (* patomic_opsig_transaction_tabort_t) (unsigned char reason)
    ctypedef void (* patomic_opsig_transaction_tcommit_t) ()
    ctypedef void (* patomic_opsig_transaction_ttest_t) ()

    # TRANSACTION EXCLUSIVE STRUCTS

    ctypedef struct patomic_ops_transaction_flag_t:
        patomic_opsig_transaction_flag_test_t fp_test
        patomic_opsig_transaction_flag_test_set_t fp_test_set
        patomic_opsig_transaction_flag_clear_t fp_clear

    ctypedef struct patomic_ops_transaction_special_t:
        patomic_opsig_transaction_double_cmpxchg_t fp_double_cmpxchg
        patomic_opsig_transaction_multi_cmpxchg_t fp_multi_cmpxchg
        patomic_opsig_transaction_generic_t fp_generic
        patomic_opsig_transaction_generic_wfb_t fp_generic_wfb

    ctypedef struct patomic_ops_transaction_raw_t:
        patomic_opsig_transaction_tbegin_t fp_tbegin
        patomic_opsig_transaction_tabort_t fp_tabort
        patomic_opsig_transaction_tcommit_t fp_tcommit
        patomic_opsig_transaction_ttest_t fp_ttest

    # TRANSACTION STRUCTS

    ctypedef struct patomic_ops_transaction_arithmetic_t:
        # in place
        patomic_opsig_transaction_void_t fp_add
        patomic_opsig_transaction_void_t fp_sub
        patomic_opsig_transaction_void_noarg_t fp_inc
        patomic_opsig_transaction_void_noarg_t fp_dec
        patomic_opsig_transaction_void_noarg_t fp_neg
        # fetch
        patomic_opsig_transaction_fetch_t fp_fetch_add
        patomic_opsig_transaction_fetch_t fp_fetch_sub
        patomic_opsig_transaction_fetch_noarg_t fp_fetch_inc
        patomic_opsig_transaction_fetch_noarg_t fp_fetch_dec
        patomic_opsig_transaction_fetch_noarg_t fp_fetch_neg

    ctypedef struct patomic_ops_transaction_binary_t:
        # in place
        patomic_opsig_transaction_void_t fp_or
        patomic_opsig_transaction_void_t fp_xor
        patomic_opsig_transaction_void_t fp_and
        patomic_opsig_transaction_void_noarg_t fp_not
        # fetch
        patomic_opsig_transaction_fetch_t fp_fetch_or
        patomic_opsig_transaction_fetch_t fp_fetch_xor
        patomic_opsig_transaction_fetch_t fp_fetch_and
        patomic_opsig_transaction_fetch_noarg_t fp_fetch_not

    ctypedef struct patomic_ops_transaction_bitwise_t:
        patomic_opsig_transaction_test_t fp_test
        patomic_opsig_transaction_test_modify_t fp_test_compl
        patomic_opsig_transaction_test_modify_t fp_test_set
        patomic_opsig_transaction_test_modify_t fp_test_reset

    ctypedef struct patomic_ops_transaction_xchg_t:
        patomic_opsig_transaction_exchange_t fp_exchange
        patomic_opsig_transaction_cmpxchg_t fp_cmpxchg_weak
        patomic_opsig_transaction_cmpxchg_t fp_cmpxchg_strong

    ctypedef struct patomic_ops_transaction_t:
        patomic_opsig_transaction_store_t fp_store
        patomic_opsig_transaction_load_t fp_load
        patomic_ops_transaction_xchg_t xchg_ops
        patomic_ops_transaction_bitwise_t bitwise_ops
        patomic_ops_transaction_binary_t binary_ops
        patomic_ops_transaction_arithmetic_t signed_ops
        patomic_ops_transaction_arithmetic_t unsigned_ops
        # extra ops not available in implicit/explicit
        patomic_ops_transaction_special_t special_ops
        patomic_ops_transaction_flag_t flag_ops
        patomic_ops_transaction_raw_t raw_ops
