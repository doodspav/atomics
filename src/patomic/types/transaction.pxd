from align cimport *


cdef extern from "<patomic/types/transaction.h>":

    # TRANSACTION FLAG

    ctypedef unsigned char patomic_transaction_flag_t

    # TRANSACTION FLAG HOLDER

    ctypedef struct patomic_transaction_padded_flag_holder_t:
        unsigned char _padding_pre[PATOMIC_MAX_CACHE_LINE_SIZE - 1]
        patomic_transaction_flag_t flag
        unsigned char _padding_post[PATOMIC_MAX_CACHE_LINE_SIZE]

    ctypedef struct patomic_transaction_padded_flag_holder_abi_unstable_t:
        unsigned char _padding_pre[PATOMIC_MAX_CACHE_LINE_SIZE_ABI_UNSTABLE - 1]
        patomic_transaction_flag_t flag
        unsigned char _padding_post[PATOMIC_MAX_CACHE_LINE_SIZE_ABI_UNSTABLE]

    # TRANSACTION CMPXCHG

    ctypedef struct patomic_transaction_cmpxchg_t:
        void *obj
        void *expected
        const void *desired

    # TRANSACTION CONFIG

    ctypedef struct patomic_transaction_config_t:
        size_t width
        size_t attempts
        const patomic_transaction_flag_t *flag_nullable

    ctypedef struct patomic_transaction_config_wfb_t:
        size_t width
        size_t attempts
        size_t fallback_attempts
        const patomic_transaction_flag_t *flag_nullable
        const patomic_transaction_flag_t *fallback_flag_nullable

    # TRANSACTION STATUS

    ctypedef enum patomic_transaction_status_t:
        patomic_TSUCCESS = 0x0
        patomic_TABORTED = 0x1
        patomic_TABORT_EXPLICIT = 0x2  | patomic_TABORTED
        patomic_TABORT_CONFLICT = 0x4  | patomic_TABORTED
        patomic_TABORT_CAPACITY = 0x8  | patomic_TABORTED
        patomic_TABORT_NESTED   = 0x10 | patomic_TABORTED
        patomic_TABORT_DEBUG    = 0x20 | patomic_TABORTED
        patomic_TABORT_INT      = 0x40 | patomic_TABORTED

    # TRANSACTION RESULT

    ctypedef struct patomic_transaction_result_t:
        unsigned int status
        size_t attempts_made

    ctypedef struct patomic_transaction_result_wfb_t:
        unsigned int status
        unsigned int fallback_status
        size_t attempts_made
        size_t fallback_attempts_made

    # TRANSACTION RECOMMENDED

    ctypedef struct patomic_transaction_recommended_t:
        size_t max_rmw_memory
        size_t max_load_memory
        size_t min_rmw_attempts
        size_t min_load_attempts

    # TRANSACTION SAFE STRING

    ctypedef struct patomic_transaction_safe_string_t:
        int required
        void * (* fp_memcpy) (void *dst, const void *src, size_t len_)
        void * (* fp_memmove) (void *dst, const void *src, size_t len_)
        void * (* fp_memset) (void *dst, int value, size_t len_)
        int (* fp_memcmp) (const void *lhs, const void *rhs, size_t len_)
