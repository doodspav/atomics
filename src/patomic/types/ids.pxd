cdef extern from "<patomic/types/ids.h>":

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
        patomic_kind_UNKN = 0x0
        patomic_kind_DYN  = 0x1
        patomic_kind_OS   = 0x2
        patomic_kind_LIB  = 0x4
        patomic_kind_BLTN = 0x8
        patomic_kind_ASM  = 0x10
        # kinds - multiple bits
        patomic_kinds_ALL = patomic_kind_DYN  | \
                            patomic_kind_OS   | \
                            patomic_kind_LIB  | \
                            patomic_kind_BLTN | \
                            patomic_kind_ASM

    # IMPLEMENTATION GET

    unsigned long patomic_get_ids(unsigned int kinds)
    unsigned int patomic_get_kind(unsigned long id_)
