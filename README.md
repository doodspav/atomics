# atomics
This library implements a wrapper around the lower level 
[patomic](https://github.com/doodspav/patomic) C library (which is provided as
part of this library through the `build_patomic` command in `setup.py`).

It exposes hardware level lock-free (and address-free) atomic operations on a 
memory buffer, either internally allocated or externally provided.

These operations are both thread-safe and process-safe, meaning that they can
be used on a shared memory buffer for interprocess communication.

## Table of Contents
<!--ts-->
* [Examples](#examples)
  * [Incorrect](#incorrect)
  * [Multi-Threading](#multi-threading)
  * [Multi-Processing](#multi-processing)
* [Docs](#docs)
  * [Types](#types)
  * [Construction](#construction)
  * [Lifetime](#lifetime)
    * [Contract](#contract)
  * [Alignment](#alignment)
  * [Properties](#properties)
  * [Operations](#operations)
  * [Special Methods](#special-methods)
  * [Memory Order](#memory-order)
  * [Exceptions](#exceptions)
* [Building](#building)
* [Future Thoughts](#future-thoughts)
* [Contributing](#contributing)
<!--te-->

## Examples

### Incorrect
The following example has a data race. It is not correct, and `a`'s value will
not equal `total` at the end.
```python
from threading import Thread


a = 0


def fn(n: int) -> None:
    global a
    for _ in range(n):
        a += 1


if __name__ == "__main__":
    # setup
    total = 10_000_000
    # run threads to completion
    t1 = Thread(target=fn, args=(total // 2,))
    t2 = Thread(target=fn, args=(total // 2,))
    t1.start(), t2.start()
    t1.join(), t2.join()
    # print results
    print(f"a[{a}] != total[{total}]")
```

### Multi-Threading
```python
import atomics
from threading import Thread


def fn(ai: atomics.INTEGRAL, n: int) -> None:
    for _ in range(n):
        ai.inc()


if __name__ == "__main__":
    # setup
    a = atomics.atomic(width=4, atype=atomics.INT)
    total = 10_000
    # run threads to completion
    t1 = Thread(target=fn, args=(a, total // 2))
    t2 = Thread(target=fn, args=(a, total // 2))
    t1.start(), t2.start()
    t1.join(), t2.join()
    # print results
    print(f"a[{a.load()}] == total[{total}]")
```

### Multi-Processing
```python
import atomics
from multiprocessing import Process, shared_memory


def fn(shmem_name: str, width: int, n: int) -> None:
    shmem = shared_memory.SharedMemory(name=shmem_name)
    buf = shmem.buf[:width]
    with atomics.atomicview(buffer=buf, atype=atomics.INT) as a:
        for _ in range(n):
            a.inc()
    del buf
    shmem.close()


if __name__ == "__main__":
    # setup
    width = 4
    shmem = shared_memory.SharedMemory(create=True, size=width)
    buf = shmem.buf[:width]
    total = 10_000
    # run processes to completion
    p1 = Process(target=fn, args=(shmem.name, width, total // 2))
    p2 = Process(target=fn, args=(shmem.name, width, total // 2))
    p1.start(), p2.start()
    p1.join(), p2.join()
    # print results and cleanup
    with atomics.atomicview(buffer=buf, atype=atomics.INT) as a:
        print(f"a[{a.load()}] == total[{total}]")
    del buf
    shmem.close()
    shmem.unlink()
```
**NOTE:** Although `shared_memory` is showcased here, `atomicview` accepts any
type that supports the buffer protocol as its buffer argument, so other sources
of shared memory such as `mmap` could be used instead.

## Docs

### Types
The following helper (abstract-ish base) types are available in `atomics`:
- [`ANY`, `INTEGRAL`, `BYTES`, `INT`, `UINT`]

This library provides the following `Atomic` classes in `atomics.base`:
- `Atomic --- ANY`
- `AtomicIntegral --- INTEGRAL`
- `AtomicBytes --- BYTES`
- `AtomicInt --- INT`
- `AtomicUint --- UINT`

These `Atomic` classes are constructable on their own, but it is strongly 
suggested using the `atomic()` function to construct them. Each class 
corresponds to one of the above helper types (as indicated).

This library also provides `Atomic*View` (in `atomics.view`) and 
`Atomic*ViewContext` (in `atomics.ctx`) counterparts to the `Atomic*` classes, 
corresponding to the same helper types. 

The latter of the two sets of classes can be constructed manually, although it
is strongly suggested using the `atomicview()` function to construct them. The 
former set of classes cannot be constructed manually with the available types,
and should only be obtained by called `.__enter__()` on a corresponding
`Atomic*ViewContext` object.

Even though you should never need to directly use these classes (apart from the
helper types), they are provided to be used in type hinting. The inheritance
hierarchies are detailed in the [ARCHITECTURE.md](ARCHITECTURE.md) file.

### Construction
This library provides the functions `atomic` and `atomicview`, along with the 
types `BYTES`, `INT`, and `UINT` (as well as `ANY` and `INTEGRAL`) to construct 
atomic objects like so:
```python
import atomics

a = atomics.atomic(width=4, atype=atomics.INT)
print(a)  # AtomicInt(value=0, width=4, readonly=False, signed=True)

buf = bytearray(2)
with atomics.atomicview(buffer=buf, atype=atomics.BYTES) as a:
    print(a)  # AtomicBytesView(value=b'\x00\x00', width=2, readonly=True)
```
You should only need to construct objects with an `atype` of `BYTES`, `INT`, or
`UINT`. Using an `atype` of `ANY` or `INTGERAL` will require additional kwargs,
and an `atype` of `ANY` will result in an object that doesn't actually expose
any atomic operations (only properties, explained in sections further on).

The `atomic()` function returns a corresponding `Atomic*` object.

The `atomicview()` function returns a corresponding `Atomic*ViewContext` object.
You can use this context object in a `with` statement to obtain an `Atomic*View`
object.

Construction can raise `UnsupportedWidthException` and `AlignmentError`.

**NOTE:** the `width` property of `Atomic*View` objects is derived from the 
buffer's length as if it were contiguous. It is equivalent to calling
`memoryview(buf).nbytes`.

### Lifetime
Objects of `Atomic*` classes (i.e. objects returned by the `atomic()` function)
have a self-contained buffer which is automatically freed. They can be passed
around and stored liked regular variables, and there is nothing special about
their lifetime.

Objects of `Atomic*ViewContext` classes (i.e. objects returned by the
`atomicview()` function) and `Atomic*View` objects obtained from said objects
have a much stricter usage contract.

#### Contract

The buffer used to construct an `Atomic*ViewContext` object (either directly or
through `atomicview()`) **MUST NOT** be invalidated until `.release()` is 
called. This is aided by the fact that `.release()` is called automatically
in `.__exit__(...)` and `.__del__()`. As long as you immediately use the context
object in a `with` statement, and **DO NOT** invalidate the buffer inside that
`with` scope, you will always be safe.

The protections implemented are shown in this example:
```python
import atomics


buf = bytearray(4)
ctx = atomics.atomicview(buffer=buf, atype=atomics.INT)

# ctx.release() here will cause ctx.__enter__() to raise:
# ValueError("Cannot open context after calling 'release'.")

with ctx as a:  # this calls ctx.__enter__()
    # ctx.release() here will raise:
    # ValueError("Cannot call 'release' while context is open.")

    # ctx.__enter__() here will raise:
    # ValueError("Cannot open context multiple times.")
    
    print(a.load())  # ok

# ctx.__exit__(...) now called
# we can safely invalidate object 'buf' now

# ctx.__enter__() will raise:
# ValueError("Cannot open context after calling 'release'.")

# accessing object 'a' in any way will also raise an exception
```

Furthermore, in CPython, all built-in types supporting the buffer protocol will
throw a `BufferError` exception if you try to invalidate them while they're in
use (i.e. before calling `.release()`).

As a last resort, if you absolutely must invalidate the buffer inside the `with`
context (where you can't call `.release()`), you may call `.__exit__(...)`
manually on the `Atomic*ViewContext` object. This is to force explicitness 
about something considered to be bad practice and dangerous.

Where it's allowed, `.release()` may be called multiple times with no
ill-effects. This also applies to `.__exit__(...)`, which has no restrictions
on where it can be called.

### Alignment
Different platforms may each have their own alignment requirements for atomic
operations of given widths. This library provides the `Alignment` class in
`atomics` to ensure that a given buffer meets these requirements.
```python
from atomics import Alignment

buf = bytearray(8)
align = Alignment(len(buf))
assert align.is_valid(buf)
```
If an atomic class is constructed from a misaligned buffer, the constructor will
raise `AlignmentError`.

By default, `.is_valid` calls `.is_valid_recommended`. The class `Alignment` 
also exposes `.is_valid_minimum`. Currently, no atomic class makes use of the
minimum alignment, so checking for it is pointless. Support for it will be 
added in a future release.

### Properties

All `Atomic*` and `Atomic*View` classes have the following properties:
- `width`: width in bytes of the underlying buffer (as if it were contiguous)
- `readonly`: whether the object supports modifying operations
- `ops_supported`: a sorted list of `OpType` enum values representing which 
  operations are supported on the object

Integral `Atomic*` and `Atomic*View` classes also have the following property:
- `signed`: whether arithmetic operations are signed or unsigned

In both cases, the behaviour on overflow is defined to wraparound.

### Operations

Base `Atomic` and `AtomicView` objects (corresponding to `ANY`) expose no atomic
operations.

`AtomicBytes` and `AtomicBytesView` objects support the following operations:
- **[base]**: `load`, `store`
- **[xchg]**: `exchange`, `cmpxchg_weak`, `cmpxchg_strong`
- **[bitwise]**: `bit_test`, `bit_compl`, `bit_set`, `bit_reset`
- **[binary]**: `bin_or`, `bin_xor`, `bin_and`, `bin_not`
- **[binary]**: `bin_fetch_or`, `bin_fetch_xor`, `bin_fetch_and`, 
  `bin_fetch_not`

Integral `Atomic*` and `Atomic*View` classes additionally support the following
operations:
- **[arithmetic]**: `add`, `sub`, `inc`, `dec`, `neg`
- **[arithmetic]**: `fetch_add`, `fetch_sub`, `fetch_inc`, `fetch_dec`, 
  `fetch_neg`

The usage of (most of) these functions is modelled directly on the C++11 
`std::atomic` implementation found 
[here](https://en.cppreference.com/w/cpp/atomic/atomic). The single notable
difference is the `cmpxchg_*` functions, which return a 2 element tuple. The
first element is a `bool` representing whether the operation succeeded, and the
second element is the original value of the object.

All operations can raise `UnsupportedOperationException` (so check 
`.ops_supported` if you need to be sure).

Operations `load`, `store`, and `cmpxchg_*` can raise `MemoryOrderError` if
called with an invalid memory order. `MemoryOrder` enum values expose the
functions `is_valid_store_order()`, `is_valid_load_order()`, and
`is_valid_fail_order()` to check with.

### Special Methods
`AtomicBytes` and `AtomicBytesView` implement the `__bytes__` special method.

Integral `Atomic*` and `Atomic*View` classes implement the `__int__` special
method. They intentionally do not implement `__index__`.

There is a notable lack of any classes implementing special methods 
corresponding to atomic operations; this is intentional. Assignment in Python is
not available as a special method, and we do not want to encourage people to
use other special methods with this class, lest it lead to them accidentally
using assignment when they meant `.store(...)`.

### Memory Order

The `MemoryOrder` enum class is provided in `atomics`, and the memory orders 
are directly copied from C++11's `std::memory_order` documentation found 
[here](https://en.cppreference.com/w/cpp/atomic/memory_order), except for 
`CONSUME` (which would be pointless to expose in this library).

All operations have a default memory order, `SEQ_CST`. This will enforce 
sequential consistency, and essentially make your multi-threaded and/or 
multi-processed program be as correct as if it were to run in a single thread.

The following helper functions are provided:
- `.is_valid_store_order()` (for `store` op)
- `.is_valid_load_order()` ( for `load` op)
- `.is_valid_fail_order()` (for the `fail` ordering in `cmpxchg_*` ops)

**IF YOU DO NOT UNDERSTAND THE LINKED DOCUMENTATION, DO NOT USE YOUR OWN
MEMORY ORDERS!!!**
Stick with the defaults to be safe. (And realistically, this is Python, you 
won't get a noticeable performance boost from using a more lax memory order).

### Exceptions
The following exceptions are available in `atomics.exc`:
- `AlignmentError`
- `MemoryOrderError`
- `UnsupportedWidthException`
- `UnsupportedOperationException`

## Building
Using `setup.py`'s `build` or `bdist_wheel` commands will run the 
`build_patomic` command (which you can also run directly).

This clones the `patomic` library into a temporary directory, builds it, and
then copies the shared library into `atomics._clib`.

This requires that `git` be installed on your system (a requirement of the
`GitPython` module). You will also need an ANSI/C90 compliant C compiler
(although ideally a more recent compiler should be used). `CMake` is also 
required but should be automatically `pip install`'d if not available.

If you absolutely cannot get `build_patomic` to work, go to
[patomic](https://github.com/doodspav/patomic), follow the instructions on
building it (making sure to build the shared library version), and then
copy-paste the shared library file into `atomics._clib` manually.

## Future Thoughts
- add support for `minimum` alignment
- add support for constructing `Atomic` classes' buffers in shared memory
- add support for passing `Atomic` objects to sub-processes and sub-interpreters

## Contributing
I don't have a guide for contributing yet. This section is here to make the 
following two points:
- new operations must first be implemented in `patomic` before this library can
be updated
- new architectures must be supported in `patomic` (no change required in this
library)
