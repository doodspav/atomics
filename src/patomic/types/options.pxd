cdef extern from "<patomic/types/options.h>":

    # OPTIONS

    ctypedef enum patomic_option_t:
        # option - single bit
        patomic_option_NONE
        # options - multiple bits
