import pathlib
import tempfile

from setuptools import Extension, setup
from Cython.Build import cythonize


# required patomic versions
patomic_version_major = 0
patomic_version_minor = 5
patomic_version_patch = 1


# currently version is required to match exactly
cython_patomic_version_check = f"""
cdef extern from *: 
    \"""
    #include <patomic/patomic_version.h>
    
    #if PATOMIC_VERSION_MAJOR != {patomic_version_major}
        #error Incompatible patomic major version. Required: =={patomic_version_major}.
    #elif PATOMIC_VERSION_MINOR != {patomic_version_minor}
        #error Incompatible patomic minor version. Required: =={patomic_version_minor}.
    #elif PATOMIC_VERSION_PATCH != {patomic_version_patch}
        #error Incompatible patomic patch version. Required: =={patomic_version_patch}.
    #endif
    \"""
"""


# installed patomic paths
include_dir = pathlib.Path.cwd().joinpath("ext/patomic/installdir/include").absolute()
library_dir = pathlib.Path.cwd().joinpath("ext/patomic/installdir/lib").absolute()


with tempfile.TemporaryDirectory(suffix="__cython") as td:

    vc_name = "patomic_version_check.pyx"
    vc_path = pathlib.Path(td).joinpath(vc_name)

    with open(vc_path, "w+") as f:
        f.write(cython_patomic_version_check)

    extensions = []
    extension_paths = [
        "src/atomics/_atomics/atomics.pyx",
        "src/atomics/_atomics/enums.pyx",
    ]

    for ep in extension_paths:
        ext = Extension(
            name=str(pathlib.Path(ep).stem),
            sources=[ep, str(vc_path)],
            include_dirs=[str(include_dir)],
            library_dirs=[str(library_dir)],
            libraries=["patomic"]
        )
        extensions.append(ext)

    setup(
        ext_modules=cythonize(extensions, language_level=3)
    )
