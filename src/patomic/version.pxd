cdef extern from "<patomic/patomic_version.h>" nogil:

    const char * PATOMIC_VERSION

    int PATOMIC_VERSION_MAJOR
    int PATOMIC_VERSION_MINOR
    int PATOMIC_VERSION_PATCH

    int patomic_version_major()
    int patomic_version_minor()
    int patomic_version_patch()

    int patomic_version_compatible_with(int major, int minor)
