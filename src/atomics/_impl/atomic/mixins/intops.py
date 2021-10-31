from ...enums import MemoryOrder, OpType

from .byteops import ByteOperationsMixin

import sys
from typing import Optional, Tuple


class IntegralOperationsMixin(ByteOperationsMixin):

    signed: bool

    def _impl_cmpxchg(self, optype: OpType, expected: int, desired: int,
                      succ: MemoryOrder, fail: MemoryOrder) -> Tuple[bool, int]:
        expected = expected.to_bytes(self.width, sys.byteorder, signed=self.signed)
        desired = desired.to_bytes(self.width, sys.byteorder, signed=self.signed)
        ok, exp = super()._impl_cmpxchg(optype, expected, desired, succ, fail)
        exp = int.from_bytes(exp, sys.byteorder, signed=self.signed)
        return ok, exp

    def _impl_bin_ari(self, optype: OpType, value: Optional[int],
                      order: MemoryOrder) -> Optional[int]:
        if value is not None:
            value = value.to_bytes(self.width, sys.byteorder, signed=self.signed)
        res = super()._impl_bin_ari(optype, value, order)
        if res is not None:
            res = int.from_bytes(res, sys.byteorder, signed=self.signed)
        return res

    def store(self, desired: int, order: MemoryOrder = MemoryOrder.SEQ_CST) -> None:
        desired = desired.to_bytes(self.width, sys.byteorder, signed=self.signed)
        super().store(desired, order)

    def load(self, order: MemoryOrder = MemoryOrder.SEQ_CST) -> int:
        value = super().load(order)
        return int.from_bytes(value, sys.byteorder, signed=self.signed)

    def exchange(self, desired: int, order: MemoryOrder = MemoryOrder.SEQ_CST) -> int:
        desired = desired.to_bytes(self.width, sys.byteorder, signed=self.signed)
        value = super().exchange(desired, order)
        return int.from_bytes(value, sys.byteorder, signed=self.signed)

    def cmpxchg_weak(self, expected: int, desired: int,
                     success: MemoryOrder = MemoryOrder.SEQ_CST,
                     failure: MemoryOrder = MemoryOrder.SEQ_CST) -> Tuple[bool, int]:
        return self._impl_cmpxchg(OpType.CMPXCHG_WEAK, expected, desired, success, failure)

    def cmpxchg_strong(self, expected: int, desired: int,
                       success: MemoryOrder = MemoryOrder.SEQ_CST,
                       failure: MemoryOrder = MemoryOrder.SEQ_CST) -> Tuple[bool, int]:
        return self._impl_cmpxchg(OpType.CMPXCHG_STRONG, expected, desired, success, failure)

    def bin_or(self, value: int, order: MemoryOrder = MemoryOrder.SEQ_CST) -> None:
        return self._impl_bin_ari(OpType.OR, value, order)

    def bin_xor(self, value: int, order: MemoryOrder = MemoryOrder.SEQ_CST) -> None:
        return self._impl_bin_ari(OpType.XOR, value, order)

    def bin_and(self, value: int, order: MemoryOrder = MemoryOrder.SEQ_CST) -> None:
        return self._impl_bin_ari(OpType.AND, value, order)

    def bin_not(self, order: MemoryOrder = MemoryOrder.SEQ_CST) -> None:
        return self._impl_bin_ari(OpType.NOT, None, order)

    def bin_fetch_or(self, value: int, order: MemoryOrder = MemoryOrder.SEQ_CST) -> int:
        return self._impl_bin_ari(OpType.FETCH_OR, value, order)

    def bin_fetch_xor(self, value: int, order: MemoryOrder = MemoryOrder.SEQ_CST) -> int:
        return self._impl_bin_ari(OpType.FETCH_XOR, value, order)

    def bin_fetch_and(self, value: int, order: MemoryOrder = MemoryOrder.SEQ_CST) -> int:
        return self._impl_bin_ari(OpType.FETCH_AND, value, order)

    def bin_fetch_not(self, order: MemoryOrder = MemoryOrder.SEQ_CST) -> int:
        return self._impl_bin_ari(OpType.FETCH_NOT, None, order)

    def add(self, value: int, order: MemoryOrder = MemoryOrder.SEQ_CST) -> None:
        return self._impl_bin_ari(OpType.ADD, value, order)

    def sub(self, value: int, order: MemoryOrder = MemoryOrder.SEQ_CST) -> None:
        return self._impl_bin_ari(OpType.SUB, value, order)

    def inc(self, order: MemoryOrder = MemoryOrder.SEQ_CST) -> None:
        return self._impl_bin_ari(OpType.INC, None, order)

    def dec(self, order: MemoryOrder = MemoryOrder.SEQ_CST) -> None:
        return self._impl_bin_ari(OpType.DEC, None, order)

    def neg(self, order: MemoryOrder = MemoryOrder.SEQ_CST) -> None:
        return self._impl_bin_ari(OpType.NEG, None, order)

    def fetch_add(self, value: int, order: MemoryOrder = MemoryOrder.SEQ_CST) -> int:
        return self._impl_bin_ari(OpType.FETCH_ADD, value, order)

    def fetch_sub(self, value: int, order: MemoryOrder = MemoryOrder.SEQ_CST) -> int:
        return self._impl_bin_ari(OpType.FETCH_SUB, value, order)

    def fetch_inc(self, order: MemoryOrder = MemoryOrder.SEQ_CST) -> int:
        return self._impl_bin_ari(OpType.FETCH_INC, None, order)

    def fetch_dec(self, order: MemoryOrder = MemoryOrder.SEQ_CST) -> int:
        return self._impl_bin_ari(OpType.FETCH_DEC, None, order)

    def fetch_neg(self, order: MemoryOrder = MemoryOrder.SEQ_CST) -> int:
        return self._impl_bin_ari(OpType.FETCH_NEG, None, order)
