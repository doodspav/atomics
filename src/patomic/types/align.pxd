cdef extern from "<patomic/types/align.h>" nogil:

    # ALIGN

    ctypedef struct patomic_align_t:
        size_t recommended
        size_t minimum
        size_t size_within

    # ALIGN CACHE LINE

    int PATOMIC_MAX_CACHE_LINE_SIZE
    int PATOMIC_MAX_CACHE_LINE_SIZE_ABI_UNSTABLE

    size_t patomic_cache_line_size()

    # ALIGN CHECKS

    int patomic_align_meets_recommended(const void *ptr, patomic_align_t align)
    int patomic_align_meets_minimum(const void *ptr, patomic_align_t align, size_t width)
