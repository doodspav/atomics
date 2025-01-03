# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.3] [Patch] - 2025-01-03
### Fixed:
- Properly pin `patomic` version to `v0.2.2` even if `patomic` has a stable
  release (which it now does)

## [1.0.2] [Patch] - 2021-12-10
### Changed
- freeze default `patomic` version to `v0.2.2` until `patomic` has a stable 
  release (to allow for breaking changes in `devel` branch)

## [1.0.1] [Patch] - 2021-11-15
### Added
- Verbosity now obtained from `-v`/`-verbose` flags (removed `-log-level` flag)
- Added `-linker-args` flag to user options (with `-l` as shortcut)
### Removed
- `-log-level` option
### Changed
- `-l` is now `-linker-args` rather than `log-level`
### Fixed:
- Filled in missing details in `setup.cfg` for older build systems:
  - Specified `build-backend` option as `setuptools.build_meta`
  - Added `install_requires` and `setup_requires`
- `cmake_args` option in `build_patomic` command now actually used


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