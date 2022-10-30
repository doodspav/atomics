from .types.align cimport *
from .types.memory_order cimport *
from .types.ops cimport *
from .types.transaction cimport *


cdef extern from "<patomic/patomic.h>" nogil:

    # ATOMIC STRUCTS

    ctypedef struct patomic_t:
        patomic_ops_t ops
        patomic_align_t align

    ctypedef struct patomic_explicit_t:
        patomic_ops_explicit_t ops
        patomic_align_t align

    ctypedef struct patomic_transaction_t:
        patomic_ops_transaction_t ops
        patomic_align_t align
        patomic_transaction_recommended_t recommended
        patomic_transaction_safe_string_t sstring

    # COMBINE

    void patomic_combine(patomic_t *priority, const patomic_t *other)
    void patomic_combine_explicit(patomic_explicit_t *priority, const patomic_explicit_t *other)

    # CREATE

    patomic_t patomic_create(
        size_t byte_width,
        patomic_memory_order_t order,
        unsigned int opts,
        unsigned int kinds,
        unsigned long ids
    )

    patomic_explicit_t patomic_create_explicit(
        size_t byte_width,
        unsigned int opts,
        unsigned int kinds,
        unsigned long ids
    )

    patomic_transaction_t patomic_create_transaction(
        unsigned int opts,
        unsigned int kinds,
        unsigned long ids
    )