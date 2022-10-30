from patomic.patomic cimport *


cpdef version():
    return PATOMIC_VERSION

cpdef version_major():
    return PATOMIC_VERSION_MAJOR

cpdef version_minor():
    return PATOMIC_VERSION_MINOR

cpdef version_patch():
    return PATOMIC_VERSION_PATCH

cpdef version_compatible_with(int major, int minor):
    return bool(patomic_version_compatible_with(major, minor))
