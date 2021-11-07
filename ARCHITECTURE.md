# Architecture

The purpose of this document is to provide a high level overview of the project
structure. It will highlight the key components, and show how they fit together.
It will also give an overview of the lifetimes of atomic objects.

It should be noted that this library does not implement any atomic 
operations itself; it wraps the [patomic](https://github.com/doodspav/patomic) 
library (implemented in C).

## Table of Contents
<!--ts-->
* [File Structure](#file-structure)
* [Composition](#composition)
* [Inheritance](#inheritance)
* [Construction and Typing](#construction-and-typing)
* [Lifetimes](#lifetimes)
<!--te-->

## File Structure
```
[project]
│
└───[src/atomics]
    │
    └───[_clib]
    └───[_impl]
        │
        └───[atomic]
            │
            └───[mixins]
```
#### [atomics.atomic]
This directory holds the implementation of all atomic classes and directly
related atomic helper functions.

#### [atomics.atomic.mixins]
This directory holds the classes implementing all atomic operations and 
properties, which are then inherited by the atomic classes. No classes here 
are designed to be constructed as is.

#### [atomics._impl]
This directory holds the building block classes which are used in atomic 
classes but can also be used as unrelated standalone classes. This includes
enum and exception classes.

#### [atomics._clib]
This directory exists solely to contain the `patomic` shared library file. This
file is generated and placed here using the `build_patomic` command from 
`setup.py`, however it can also be built and placed here manually.

#### [atomics]
Nothing is implemented at this level. All files here exist to nicely partition
the implemented types for the end user.

## Composition

The two key classes at the base of atomic objects are `PyBuffer` and 
`Patomic`. These are combined in the `AtomicCore` class.

```
AtomicCore
│
└───obj(Ops) - - - (from Patomic)
└───obj(PyBuffer)
```

#### Patomic
This class exposes all the visible symbols and types in the `patomic` library 
for use in Python.

#### PyBuffer
This class is used to access the `width`, `address`, and `readonly` attributes
of the underlying buffer of any object supporting the buffer protocol.

#### AtomicCore
This class is the core attribute present in the `Atomic`, `AtomicView`, and
`AtomicViewContext` classes.  
It stores an `Ops` object (obtained from `Patomic`) in order to access all the 
operations in the C library, and a `PyBuffer` object to perform the operations
on. All atomic related operations pass through it.

## Inheritance

#### [atomics.atomic.mixins]
Mixins provides the following 5 classes, implementing all relevant atomic 
properties and operations, with the following inheritance hierarchy:

```
ANY
│
└───BYTES
│
└───INTEGRAL
    │
    └───INT
    └───UINT
```

#### [atomics.atomic]

The files here provide the following 5 `AtomicViewContext` classes, which follow
the same inheritance hierarchy as the mixin classes:
```
AtomicViewContext
│
└───AtomicBytesViewContext
│
└───AtomicIntegralViewContext
    │
    └───AtomicIntViewContext
    └───AtomicUintViewContext
```

The files also provide `Atomic` and `AtomicView` classes with the same naming 
scheme as `AtomicViewContext`. They also follow the same inheritance 
hierarchy except that they additionally inherit from the appropriate mixin 
class, as shown below using `Atomic`:
```
Atomic <--- ANY
│
└───AtomicBytes <--- BYTES
│
└───AtomicIntegral <--- INTEGRAL
    │
    └───AtomicInt <--- INT
    └───AtomicUint <--- UINT
```

## Construction and Typing

This section covers `Atomic`, `AtomicView`, `AtomicViewContext` classes (and 
their children), and the mixin classes `ANY`, `INTEGRAL`, `BYTES`, `INT`, and 
`UINT`.

None of the atomic classes mentioned above are intended for the user to 
construct manually. The helper functions `atomic` and `atomicview` are provided
for this purpose, which construct `Atomic` and `AtomicViewContext` objects
respectively.

The atomic and mixin classes are exposed to the user for the purpose of being
used as type hints.

The `Atomic` and `AtomicViewContext` classes (and their children) **MAY** be
constructed manually by the user. The `AtomicView` classes (and their children)
and the mixin classes are **NOT** intended to be constructed manually by the
user.

## Lifetimes

`Atomic` classes have no explicit lifetime requirements. They may be passed 
around and used as a normal variable.

`AtomicView` classes are obtained by `AtomicViewContext.__enter__()` and must
not be used after `AtomicViewContext.release()` has been called (which is 
called in `AtomicViewContext.__exit__(...)` and `.__del__()`.)

`AtomicViewContext` classes are constructed from an externally provided buffer.
This buffer **MUST NOT** be invalidated from the time the `AtomicViewContext` 
instance has been initialised, until `.release()` is called on the instance 
(either directly or indirectly).

An exception to this is if `.release()` is guaranteed to be called before
`.__enter__()` is called (in which case the `AtomicView` object is never 
obtained). In this case, the buffer may be invalidated at any time after
initialisation.
