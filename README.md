# atomics
This library implements a wrapper around the lower level 
[patomic](https://github.com/doodspav/patomic) C library
(which is provided as part of this library, cloned in `setup.py`).

It exposes hardware level lock-free (and address-free) atomic 
operations on a memory buffer, either internally allocated or 
externally provided. 

These operations are both thread-safe and
process-safe, meaning they can be used on shared memory buffers.

## Table of Contents
<!--ts-->
* [Atomic](#atomic)
  * [Construction](#construction)
  * [Operations](#operations)
  * [Helpers](#helpers)
* [Alignment](#alignment)
* [Exceptions](#exceptions)
* [Lifetime](#lifetime)
* [Examples](#examples)
  * [From Width](#from-width)
  * [From Buffer](#from-buffer)
* [Building Manually](#building-manually)
* [Additional Operations and Platform Support](#additional-operations-and-platform-support)
<!--te-->

## Atomic
This package provides the following three classes providing atomic operations:
- `AtomicBytes`
- `AtomicInt`
- `AtomicUint`

### Construction
All three classes can be constructed from either an object supporting the buffer
protocol (such as `bytes`, `bytearray`, or `memoryview`), or an `int`.

If constructed from an object supporting the buffer protocol, the internal buffer
of the object is interpreted as a `char[]`The length of this array is equivalent
to `memoryview(obj).nbytes` which is not necessarily `len(obj)`. If the object is
readonly, then the `Atomic` class will also be readonly.

If constructed from an `int` object, an internal suitably aligned buffer will be
allocated with a width of that object. The internal buffer will be allocated in
process-local memory.

The available constructors for all `Atomic` classes are listed below (using 
`__init__` directly is not recommended, for readability reasons).
```python
def __init__(self, *, buffer_or_width):
    pass

@classmethod
def from_buffer(buffer):
    pass

@classmethod
def from_width(width: int):
    pass
```

Construction may raise `UnsupportedWidthException` or `AlignmentError`.

### Operations
All three `Atomic` classes provide may provide the following operations:
- `load`, `store`
- `exchange`, `cmpxchg_weak`, `cmpxchg_strong`
- `bit_test`, `bit_test_compl`, `bit_test_set`, `bit_test_reset`
- `bin_or`, `bin_xor`, `bin_and`, `bin_not`

`AtomicInt` and `AtomicUint` additionally provide:
- `add`, `sub`, `inc`, `dec`, `neg`

**IMPORTANT:**

No operations are guaranteed to exist, even if you expect them to. It is 
possible for non-modifying operations to be available on a mutable `Atomic` 
object, but not on a readonly one. You should always check that an operation
is supported before calling it (using `.ops_supported`, mentioned below). 
Calling an unsupported operation will raise `UnsupportedOperationException`. 

Binary and arithmetic operations also have `fetch` variants which return the
value before the operation (e.g. `bin_fetch_or`, `fetch_add`).
All mutating operations returning a value will return the value as it was
before any operation took place (hence the order in the words `read-modify-write`).

The parameters for these functions are based directly on the named operations
in C++'s [std::atomic](https://en.cppreference.com/w/cpp/atomic/atomic).

### Helpers
- `.width` - the length in bytes of the underlying buffer
- `.readonly` - whether modifying operations are available
- `.ops_supported` - list of enum values representing supported operations
- `.signed` - whether the integer is signed (not available for `AtomicBytes`)

## MemoryOrder
The default memory order for all operations is `MemoryOrder.SEQ_CST`. Using this
order, all operations will be seen to take place as if the program is single
threaded.

Using a weaker memory order is risky, and can lead to incorrect programs with
inconsistent state. The documentation for memory orders is 
[here](https://en.cppreference.com/w/cpp/atomic/memory_order). If you don't
understand that, **don't use a custom memory order**.

There is no `MemoryOrder.CONSUME`. No compiler supports it, and even if they did
it would be useless here since the compiler of the `patomic` library can't see
the caller of the functions.

## Alignment
Some platforms require that atomic operations be performed on memory with a certain
alignment. A manual check is only necessary if you provide your own buffer to the
`Atomic` class's constructor (to make sure it doesn't raise an `AlignmentError`).

The check can be performed like this:
```python
from atomics import Alignment

buffer = bytes(8)
align = Alignment(len(buffer))
assert align.is_valid(buffer)
```

This will check that your buffer meets the recommended alignment. Currently, the
`Atomic` classes don't provide a way to make use of the `minimum` alignment.

The following attributes are available on `Alignment`:
- `width`
- `recommended`
- `minimum`
- `size_within`

Their usage isn't elaborated on here since it isn't expected to be necessary
to access them directly. Details on what these represent can be found 
[here](https://github.com/doodspav/patomic/blob/devel/include/patomic/types/align.h).

## Exceptions
- `AlignmentError` - buffer doesn't meet alignment requirements
- `MemoryOrderError` - given memory order is not applicable to attempted operation
- `UnsupportedOperationException` - the operation is not supported
- `UnsupportedWidthException` - no operations are supported for the provided buffer or width

## Lifetime

The `Atomic` object **MUST NOT** outlive the buffer it acts upon. This is simple
when constructing from a width (since the buffer will be released in `__del__`),
but trickier when constructing from an external buffer. The `Atomic` object holds
an internal reference to the object whose buffer it uses, so it won't outlive
that object (just potentially its buffer).

To aid in this, `Atomic` classes define `release()`, `__enter__`, and `__exit__`.
Both `release()` and `__exit__` will release the internal buffer, meaning that the
`Atomic` object must not be used after either of these is called. `__enter__` will
simply return `self`.

## Examples

### From Width
```python
from atomics import AtomicInt


a = AtomicInt.from_width(4)
a.store(0)
a.add(5)
print(a.load())  # prints 5
# a.release() not required since we didn't construct from an external buffer
```

### From Buffer
```python
from atomics import AtomicUint
from multiprocessing import shared_memory


shmem = shared_memory.SharedMemory(create=True, size=4)

# using: .release()
a = AtomicUint.from_buffer(shmem.buf[:4])
a.store(0)
a.add(5)
print(a.load())  # prints 5
a.release()  # since an object's destructor is not called in a deterministic fashion

# using: .__enter__, .__exit__
with AtomicUint.from_buffer(shmem.buf[:4]) as a:
  a.add(5)
  print(a.load())  # prints 10
  #  a.__exit__(...) will call a.release() for us

shmem.close()
shmem.unlink()
```

## Building Manually

If you need to build a specific version of `patomic`, or need more customisation over
the build process, the custom command `build_patomic` can be used to build `patomic` 
before running the normal `build` command. Options this command accepts can be found
in `setup.py`. This command is run automatically in the default build process.

If you need even more build customisation, you can clone `patomic` and manually build
it using CMake. You must then place the resulting shared library file into
`src/atomics/_clib`.

## Additional Operations and Platform Support
All additional operations must be implemented in `patomic` before being exposed
here. Supporting additional platforms is also done in `patomic`.