from .base import AtomicView, AtomicViewContext
from .baseint import AtomicIntegralView, AtomicIntegralViewContext
from .bytes import AtomicBytesView, AtomicBytesViewContext
from .int import AtomicIntView, AtomicUintView, AtomicIntViewContext, AtomicUintViewContext

from typing import overload, Type


@overload
def atomicview(buffer, atype: Type[AtomicView], **kwargs) -> AtomicViewContext:
    ...


@overload
def atomicview(buffer, atype: Type[AtomicIntegralView], **kwargs) -> AtomicIntegralViewContext:
    ...


@overload
def atomicview(buffer, atype: Type[AtomicBytesView], **kwargs) -> AtomicBytesViewContext:
    ...


@overload
def atomicview(buffer, atype: Type[AtomicIntView], **kwargs) -> AtomicIntViewContext:
    ...


@overload
def atomicview(buffer, atype: Type[AtomicUintView], **kwargs) -> AtomicUintViewContext:
    ...


def atomicview(buffer, atype, **kwargs):
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
