cdef extern from "<patomic/patomic_version.h>":

    int PATOMIC_VERSION_MAJOR
    int PATOMIC_VERSION_MINOR
    int PATOMIC_VERSION_PATCH

    int patomic_version_major()
    int patomic_version_minor()
    int patomic_version_patch()

    int patomic_version_compatible_with(int major, int minor)

cpdef version_major():
    return PATOMIC_VERSION_MAJOR

cpdef version_minor():
    return PATOMIC_VERSION_MINOR

cpdef version_compatible_with(int major, int minor):
    return bool(patomic_version_compatible_with(major, minor))
