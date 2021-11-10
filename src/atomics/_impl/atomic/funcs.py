from .base import Atomic, AtomicViewContext
from .baseint import AtomicIntegral, AtomicIntegralViewContext
from .bytes import AtomicBytes, AtomicBytesViewContext
from .int import AtomicInt, AtomicIntViewContext
from .int import AtomicUint, AtomicUintViewContext

from .mixins.types import ANY, INTEGRAL, BYTES, INT, UINT

from typing import overload, Type, Union


ATUnion = Union[
    ANY,
    INTEGRAL,
    BYTES,
    INT,
    UINT
]

AUnion = Union[
    Atomic,
    AtomicIntegral,
    AtomicBytes,
    AtomicInt,
    AtomicUint
]

AVCUnion = Union[
    AtomicViewContext,
    AtomicIntegralViewContext,
    AtomicBytesViewContext,
    AtomicIntViewContext,
    AtomicUintViewContext
]


@overload
def atomic(width: int, atype: Type[INT], **kwargs) -> AtomicInt:
    ...


@overload
def atomic(width: int, atype: Type[UINT], **kwargs) -> AtomicUint:
    ...


@overload
def atomic(width: int, atype: Type[BYTES], **kwargs) -> AtomicBytes:
    ...


@overload
def atomic(width: int, atype: Type[INTEGRAL], **kwargs) -> AtomicIntegral:
    ...


@overload
def atomic(width: int, atype: Type[ANY], **kwargs) -> Atomic:
    ...


def atomic(width: int, atype: Type[ATUnion], **kwargs) -> AUnion:
    if atype is INT:
        return AtomicInt(width=width)
    elif atype is UINT:
        return AtomicUint(width=width)
    elif atype is BYTES:
        return AtomicBytes(width=width)
    elif atype is INTEGRAL:
        return AtomicIntegral(width=width, **kwargs)
    elif atype is ANY:
        return Atomic(width=width, **kwargs)
    else:
        msg = "Type parameter 'atype' must be one of [ANY, INTEGRAL, BYTES, INT, UINT]."
        raise TypeError(msg)


@overload
def atomicview(buffer, atype: Type[INT], **kwargs) -> AtomicIntViewContext:
    ...


@overload
def atomicview(buffer, atype: Type[UINT], **kwargs) -> AtomicUintViewContext:
    ...


@overload
def atomicview(buffer, atype: Type[BYTES], **kwargs) -> AtomicBytesViewContext:
    ...


@overload
def atomicview(buffer, atype: Type[INTEGRAL], **kwargs) -> AtomicIntegralViewContext:
    ...


@overload
def atomicview(buffer, atype: Type[ANY], **kwargs) -> AtomicViewContext:
    ...


def atomicview(buffer, atype: Type[ATUnion], **kwargs) -> AVCUnion:
    if atype is INT:
        return AtomicIntViewContext(buffer=buffer)
    elif atype is UINT:
        return AtomicUintViewContext(buffer=buffer)
    elif atype is BYTES:
        return AtomicBytesViewContext(buffer=buffer)
    elif atype is INTEGRAL:
        return AtomicIntegralViewContext(buffer=buffer, **kwargs)
    elif atype is ANY:
        return AtomicViewContext(buffer=buffer, **kwargs)
    else:
        msg = "Type parameter 'atype' must be one of [ANY, INTEGRAL, BYTES, INT, UINT]."
        raise TypeError(msg)
