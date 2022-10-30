from .ops cimport *


cdef extern from "<patomic/types/feature_check.h>":

    # OPCAT

    ctypedef enum patomic_opcat_t:
        patomic_opcat_NONE
        # opcat - single bit
        patomic_opcat_LDST
        patomic_opcat_XCHG
        patomic_opcat_BIT
        patomic_opcat_BIN_V
        patomic_opcat_BIN_F
        patomic_opcat_SARI_V
        patomic_opcat_SARI_F
        patomic_opcat_UARI_V
        patomic_opcat_UARI_F
        patomic_opcat_SPEC
        patomic_opcat_FLAG
        patomic_opcat_RAW
        # opcats - multiple bits
        patomic_opcats_BIN
        patomic_opcats_SARI
        patomic_opcats_UARI
        patomic_opcats_ARI
        patomic_opcats_IMPLICIT
        patomic_opcats_EXPLICIT
        patomic_opcats_TRANSACTION

    # OPKIND

    ctypedef enum patomic_opkind_t:
        patomic_opkind_NONE
        # base (opcat_LDST)
        patomic_opkind_LOAD
        patomic_opkind_STORE
        patomic_opkinds_LDST
        # xchg
        patomic_opkind_EXCHANGE
        patomic_opkind_CMPXCHG_WEAK
        patomic_opkind_CMPXCHG_STRONG
        patomic_opkinds_XCHG
        # bitwise and flag
        patomic_opkind_TEST
        patomic_opkind_TEST_SET
        patomic_opkind_TEST_RESET
        patomic_opkind_TEST_COMPL
        patomic_opkind_CLEAR
        patomic_opkinds_BIT
        patomic_opkinds_FLAG
        # binary
        patomic_opkind_OR
        patomic_opkind_XOR
        patomic_opkind_AND
        patomic_opkind_NOT
        patomic_opkinds_BIN
        # arithmetic
        patomic_opkind_ADD
        patomic_opkind_SUB
        patomic_opkind_INC
        patomic_opkind_DEC
        patomic_opkind_NEG
        patomic_opkinds_ARI
        # special
        patomic_opkind_DOUBLE_CMPXCHG
        patomic_opkind_MULTI_CMPXCHG
        patomic_opkind_GENERIC
        patomic_opkind_GENERIC_WFB
        patomic_opkinds_SPEC
        # raw
        patomic_opkind_TBEGIN
        patomic_opkind_TABORT
        patomic_opkind_TCOMMIT
        patomic_opkind_TTEST
        patomic_opkinds_RAW

    # FEATURE ALL

    unsigned int patomic_feature_check_all(const patomic_ops_t *ops, unsigned int opcats)
    unsigned int patomic_feature_check_all_explicit(const patomic_ops_explicit_t *ops, unsigned int opcats)
    unsigned int patomic_feature_check_all_transaction(const patomic_ops_transaction_t *ops, unsigned int opcats)

    # FEATURE ANY

    unsigned int patomic_feature_check_any(const patomic_ops_t *ops, unsigned int opcats)
    unsigned int patomic_feature_check_any_explicit(const patomic_ops_explicit_t *ops, unsigned int opcats)
    unsigned int patomic_feature_check_any_transaction(const patomic_ops_transaction_t *ops, unsigned int opcats)

    # FEATURE LEAF

    unsigned int patomic_feature_check_leaf(const patomic_ops_t *ops, unsigned int opcat, unsigned int opkinds)
    unsigned int patomic_feature_check_leaf_explicit(const patomic_ops_explicit_t *ops, unsigned int opcat, unsigned int opkinds)
    unsigned int patomic_feature_check_leaf_transaction(const patomic_ops_transaction_t *ops, unsigned int opcat, unsigned int opkinds)
