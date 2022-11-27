import pathlib
import setuptools
import tempfile

from Cython.Build import cythonize


# required patomic versions
patomic_version_major = 0
patomic_version_minor = 5
patomic_version_patch = 1


# installed patomic paths
include_dir = pathlib.Path.cwd().joinpath("ext/patomic/installdir/include").absolute()
library_dir = pathlib.Path.cwd().joinpath("ext/patomic/installdir/lib").absolute()


# extension params
extension_paths = [pathlib.Path.cwd().joinpath(ep).absolute() for ep in [
    "src/atomics/_atomics/atomics.pyx",
    "src/atomics/_atomics/enums.pyx"
]]
define_macros = [
    ("ATOMICS_PATOMIC_VERSION_MAJOR", patomic_version_major),
    ("ATOMICS_PATOMIC_VERSION_MINOR", patomic_version_minor),
    ("ATOMICS_PATOMIC_VERSION_PATCH", patomic_version_patch)
]


# we need to provide a second empty source file for each extension
# otherwise relative cimports will not work (no idea why)
with tempfile.TemporaryDirectory(suffix="__cython") as td:

    # create all extensions
    extensions = []
    for ep in extension_paths:

        # each extension module needs its own temporary path
        # if they are all the same, then we will get an error about sorting dicts
        temp_name = f"empty_{ep.stem}.pyx"
        temp_path = pathlib.Path(td).joinpath(temp_name).absolute()

        with open(temp_path, "w+") as f:
            f.write("")

        ext = setuptools.Extension(
            name=str(ep.stem),
            sources=[str(ep), str(temp_path)],
            include_dirs=[str(include_dir)],
            library_dirs=[str(library_dir)],
            libraries=["patomic"],
            define_macros=define_macros
        )
        extensions.append(ext)

    # run setup on all extensions
    setuptools.setup(
        ext_modules=cythonize(extensions, language_level=3)
    )
