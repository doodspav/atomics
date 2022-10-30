from pathlib import Path
from setuptools import Extension, setup
from Cython.Build import cythonize

include_dir = Path.cwd().joinpath("ext/patomic/installdir/include").absolute()
library_dir = Path.cwd().joinpath("ext/patomic/installdir/lib").absolute()

atomics = Extension(
    name="atomics",
    sources=["src/atomics.pyx"],
    include_dirs=[str(include_dir)],
    library_dirs=[str(library_dir)],
    libraries=["patomic"]
)

setup(
    ext_modules=cythonize(atomics, language_level=3)
)
