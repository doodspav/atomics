cdef extern from * nogil:
    """
    #include <patomic/patomic_version.h>

    #if !defined(ATOMICS_PATOMIC_VERSION_MAJOR)
        #error Required patomic major version not defined.
    #elif !defined(ATOMICS_PATOMIC_VERSION_MINOR)
        #error Required patomic minor version not defined.
    #elif !defined(ATOMICS_PATOMIC_VERSION_PATCH)
        #error Required patomic patch version not defined.
    #endif

    #if PATOMIC_VERSION_MAJOR != ATOMICS_PATOMIC_VERSION_MAJOR
        #error Incompatible required and provided patomic major version.
    #elif PATOMIC_VERSION_MINOR != ATOMICS_PATOMIC_VERSION_MINOR
        #error Incompatible required and provided patomic minor version.
    #elif PATOMIC_VERSION_PATCH != ATOMICS_PATOMIC_VERSION_PATCH
        #error Incompatible required and provided patomic patch version.
    #endif
    """
