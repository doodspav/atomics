from .base import AtomicView, AtomicViewContext
from .baseint import AtomicIntegralView, AtomicIntegralViewContext
from .bytes import AtomicBytesView, AtomicBytesViewContext
from .int import AtomicIntView, AtomicUintView, AtomicIntViewContext, AtomicUintViewContext

from typing import overload, Type, Union


AVUnion = Union[
    AtomicView,
    AtomicIntegralView,
    AtomicBytesView,
    AtomicIntView,
    AtomicUintView
]

AVCUnion = Union[
    AtomicViewContext,
    AtomicIntegralViewContext,
    AtomicBytesViewContext,
    AtomicIntViewContext,
    AtomicUintViewContext
]


@overload
def atomicview(buffer, atype: Type[AtomicIntView], **kwargs) -> AtomicIntViewContext:
    ...


@overload
def atomicview(buffer, atype: Type[AtomicUintView], **kwargs) -> AtomicUintViewContext:
    ...


@overload
def atomicview(buffer, atype: Type[AtomicBytesView], **kwargs) -> AtomicBytesViewContext:
    ...


@overload
def atomicview(buffer, atype: Type[AtomicIntegralView], **kwargs) -> AtomicIntegralViewContext:
    ...


@overload
def atomicview(buffer, atype: Type[AtomicView], **kwargs) -> AtomicViewContext:
    ...


def atomicview(buffer, atype: Type[AVUnion], **kwargs) -> AVCUnion:
    if atype is AtomicIntView:
        return AtomicIntViewContext(buffer=buffer)
    elif atype is AtomicUintView:
        return AtomicUintViewContext(buffer=buffer)
    elif atype is AtomicBytesView:
        return AtomicBytesViewContext(buffer=buffer)
    elif atype is AtomicIntegralView:
        return AtomicIntegralViewContext(buffer=buffer, **kwargs)
    elif atype is AtomicView:
        return AtomicViewContext(buffer=buffer, **kwargs)
    else:
        msg = "Type parameter 'atype' must be a provided type deriving from AtomicView."
        raise TypeError(msg)
