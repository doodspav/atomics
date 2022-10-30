cdef extern from "<patomic/types/ids.h>" nogil:

    # IMPLEMENTATION IDS

    ctypedef unsigned long patomic_id_t

    # id - single bit
    unsigned long patomic_id_NULL
    unsigned long patomic_id_STD
    unsigned long patomic_id_MSVC
    unsigned long patomic_id_GNU
    unsigned long patomic_id_TSX
    # ids - multiple bits
    unsigned long patomic_ids_ALL

    # IMPLEMENTATION KINDS

    ctypedef enum patomic_kind_t:
        # kind - single bit
        patomic_kind_UNKN
        patomic_kind_DYN
        patomic_kind_OS
        patomic_kind_LIB
        patomic_kind_BLTN
        patomic_kind_ASM
        # kinds - multiple bits
        patomic_kinds_ALL

    # IMPLEMENTATION GET

    unsigned long patomic_get_ids(unsigned int kinds)
    unsigned int patomic_get_kind(unsigned long id_)
