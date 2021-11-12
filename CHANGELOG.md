# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] [Patch]
- Small build systems patch to fix building with older tooling:
  - Specified `build-backend` option in `setup.cfg` as `setuptools.build_meta`
  - Added `install_requires` and `setup_requires` to `setup.cfg`

## [1.0.0] [Major] - 2021-11-10
### Added
- Initial release
- Implementation is Python wrapper around `patomic` C library
- Provides:
  - **.**: `atomic()`, `atomicview()`
  - **.**: `Alignment`, `CmpxchgResult`, `MemoryOrder`, `OpType`
  - **.**: `ANY`, `INTEGRAL`, `BYTES`, `INT`, `UINT`
  - **.base**: `Atomic`, `Atomic{Integral|Bytes|Int|Uint}`
  - **.view**: `AtomicView`, `Atomic{Integral|Bytes|Int|Uint}View`
  - **.ctx**: `AtomicViewContext`, `Atomic{Integral|Bytes|Int|Uint}ViewContext`
  - **.exc**: `AlignmentError`, `MemoryOrderError`,
`Unsupported{Width|Operation}Exception`
- Cmpxchg functions return `CmpxchgResult[T]` (with `T` in `[bytes, int]`)
- No testing provided