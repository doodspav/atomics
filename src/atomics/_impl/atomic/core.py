from ..enums import OpType
from ..decorators import unreleased
from ..patomic import Ops
from ..pybuffer import PyBuffer

from typing import Callable, Dict, Optional


class AtomicCore:

    def __init__(self, buffer: PyBuffer, ops: Ops, *, is_integral: bool, is_signed: bool):
        # check if object has been initialised
        if hasattr(self, "_buffer"):
            raise ValueError("Core object cannot be re-initialised.")
        # setup members
        self._buffer: PyBuffer = buffer
        self._ops: Ops = ops
        self._is_integral: bool = is_integral
        self._is_signed: bool = is_signed
        self._supported: Dict[OpType, Callable] = self._get_supported_ops_map()

    @unreleased
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def __del__(self):
        self.release()

    def __bool__(self):
        return not self._released

    def release(self) -> None:
        # this may be called in __del__ if exception is raised in __init__
        # we cannot rely on any attributes existing
        if hasattr(self, "_buffer"):
            self._buffer.release()

    @property
    def _released(self) -> bool:
        return hasattr(self, "_buffer") and self._buffer

    @unreleased
    def get_op_func(self, optype: OpType) -> Optional[Callable]:
        return self._supported.get(optype)

    @unreleased
    def _get_supported_ops_map(self) -> Dict[OpType, Callable]:
        ots: Dict[OpType, Callable] = {}
        # loop through all possible ops
        for ot in OpType:
            # ignore arithmetic ops if not integral
            if not self._is_integral and ot >= OpType.ADD:
                continue
            # ignore mutating ops if readonly
            if self._buffer.readonly and ot not in (OpType.LOAD, OpType.BIT_TEST):
                continue
            # get op category (e.g. _ops for load, _ops.xchg_ops for exchange, etc...)
            cat = self._ops
            if ot.cname is not None:
                s_type = "signed" if self._is_signed else "unsigned"
                cname = ot.cname.replace("arithmetic", s_type)
                cat = getattr(cat, cname)
            # get op function pointer
            fp = getattr(cat, ot.fname)
            # add to ots if supported (i.e. fp is not NULL)
            if fp:
                ots[ot] = fp
        # return supported ops
        return ots

    @unreleased
    @property
    def address(self) -> int:
        return self._buffer.address

    @unreleased
    @property
    def width(self) -> int:
        return self._buffer.width

    @unreleased
    @property
    def readonly(self) -> bool:
        return self._buffer.readonly

    @unreleased
    @property
    def signed(self) -> bool:
        return self._is_signed
