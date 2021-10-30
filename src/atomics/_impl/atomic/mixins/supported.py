from ...enums import OpType
from ...patomic import Ops

from typing import Callable, Dict


class SupportedMixin:

    _is_integral: bool
    _is_signed: bool
    _ops: Ops

    readonly: bool

    def __init__(self):
        ots: Dict[OpType, Callable] = {}
        # get available ops
        for ot in OpType:
            # check integral and readonly
            if not self._is_integral and ot >= OpType.ADD:
                continue
            if self.readonly and ot not in (OpType.LOAD, OpType.BIT_TEST):
                continue
            # add supported ops to dict
            cat = self._ops
            if ot.cname is not None:
                s_type = "signed" if self._is_signed else "unsigned"
                cname = ot.cname.replace("arithmetic", s_type)
                cat = getattr(cat, cname)
            op = getattr(cat, ot.fname)
            if op:
                ots[ot] = op
        # save to instance
        self._supported = ots

    @property
    def ops_supported(self) -> [OpType]:
        return sorted(list(self._supported.keys()))
