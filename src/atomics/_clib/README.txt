This directory is meant to hold the patomic shared library (usually patomic.dll, libpatomic.dylib, libpatomic.so).
This should automatically be built as a step in building a bdist_wheel or installing an sdist.
On the off chance the build fails, the library can be built manually.
The patomic source code can be found at https://github.com/doodspav/patomic (potentially only on the devel branch).
Compilation with CMake should work painlessly (the code is ANSI compatible).