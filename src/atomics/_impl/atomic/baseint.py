from .base import AtomicBase
from ..enums import MemoryOrder, OpType
from ..exceptions import MemoryOrderError

import sys
from typing import Optional, Tuple


class AtomicIntegralBase(AtomicBase):

    def __init__(self, buffer_or_width, *, is_signed: bool):
        super().__init__(buffer_or_width, is_integral=True, is_signed=is_signed)

    @property
    def signed(self) -> bool:
        return self._is_signed

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

    def _impl_cmpxchg(self, optype: OpType, expected: int, desired: int,
                      succ: MemoryOrder, fail: MemoryOrder) -> Tuple[bool, int]:
        expected = expected.to_bytes(self.width, sys.byteorder, signed=self.signed)
        desired = desired.to_bytes(self.width, sys.byteorder, signed=self.signed)
        ok, exp = super()._impl_cmpxchg(optype, expected, desired, succ, fail)
        exp = int.from_bytes(exp, sys.byteorder, signed=self.signed)
        return ok, exp

    def _impl_bin_arithmetic(self, optype: OpType, value: Optional[int],
                             order: MemoryOrder) -> Optional[int]:
        if value is not None:
            value = value.to_bytes(self.width, sys.byteorder, signed=self.signed)
        res = super()._impl_bin_ari(optype, value, order)
        if res is not None:
            res = int.from_bytes(res, sys.byteorder, signed=self.signed)
        return res

    def cmpxchg_weak(self, expected: int, desired: int,
                     success: MemoryOrder = MemoryOrder.SEQ_CST,
                     failure: MemoryOrder = MemoryOrder.SEQ_CST) -> Tuple[bool, int]:
        return self._impl_cmpxchg(OpType.CMPXCHG_WEAK, expected, desired, success, failure)

    def cmpxchg_strong(self, expected: int, desired: int,
                       success: MemoryOrder = MemoryOrder.SEQ_CST,
                       failure: MemoryOrder = MemoryOrder.SEQ_CST) -> Tuple[bool, int]:
        return self._impl_cmpxchg(OpType.CMPXCHG_STRONG, expected, desired, success, failure)

    def bit_test(self, index: int, order: MemoryOrder = MemoryOrder.SEQ_CST) -> bool:
        if not order.is_valid_store_order():
            raise MemoryOrderError(OpType.BIT_TEST, order, is_fail=False)
        return self._impl_bit_test(OpType.BIT_TEST, index, order)

    def bit_test_compl(self, index: int, order: MemoryOrder = MemoryOrder.SEQ_CST) -> bool:
        return self._impl_bit_test(OpType.BIT_TEST_COMPL, index, order)

    def bit_test_set(self, index: int, order: MemoryOrder = MemoryOrder.SEQ_CST) -> bool:
        return self._impl_bit_test(OpType.BIT_TEST_SET, index, order)

    def bit_test_reset(self, index: int, order: MemoryOrder = MemoryOrder.SEQ_CST) -> bool:
        return self._impl_bit_test(OpType.BIT_TEST_RESET, index, order)

    def bin_or(self, value: int, order: MemoryOrder = MemoryOrder.SEQ_CST) -> None:
        return self._impl_bin_arithmetic(OpType.OR, value, order)

    def bin_xor(self, value: int, order: MemoryOrder = MemoryOrder.SEQ_CST) -> None:
        return self._impl_bin_arithmetic(OpType.XOR, value, order)

    def bin_and(self, value: int, order: MemoryOrder = MemoryOrder.SEQ_CST) -> None:
        return self._impl_bin_arithmetic(OpType.AND, value, order)

    def bin_not(self, order: MemoryOrder = MemoryOrder.SEQ_CST) -> None:
        return self._impl_bin_arithmetic(OpType.NOT, None, order)

    def bin_fetch_or(self, value: int, order: MemoryOrder = MemoryOrder.SEQ_CST) -> int:
        return self._impl_bin_arithmetic(OpType.FETCH_OR, value, order)

    def bin_fetch_xor(self, value: int, order: MemoryOrder = MemoryOrder.SEQ_CST) -> int:
        return self._impl_bin_arithmetic(OpType.FETCH_XOR, value, order)

    def bin_fetch_and(self, value: int, order: MemoryOrder = MemoryOrder.SEQ_CST) -> int:
        return self._impl_bin_arithmetic(OpType.FETCH_AND, value, order)

    def bin_fetch_not(self, order: MemoryOrder = MemoryOrder.SEQ_CST) -> int:
        return self._impl_bin_arithmetic(OpType.FETCH_NOT, None, order)

    def add(self, value: int, order: MemoryOrder = MemoryOrder.SEQ_CST) -> None:
        return self._impl_bin_arithmetic(OpType.ADD, value, order)

    def sub(self, value: int, order: MemoryOrder = MemoryOrder.SEQ_CST) -> None:
        return self._impl_bin_arithmetic(OpType.SUB, value, order)

    def inc(self, order: MemoryOrder = MemoryOrder.SEQ_CST) -> None:
        return self._impl_bin_arithmetic(OpType.INC, None, order)

    def dec(self, order: MemoryOrder = MemoryOrder.SEQ_CST) -> None:
        return self._impl_bin_arithmetic(OpType.DEC, None, order)

    def neg(self, order: MemoryOrder = MemoryOrder.SEQ_CST) -> None:
        return self._impl_bin_arithmetic(OpType.NEG, None, order)

    def fetch_add(self, value: int, order: MemoryOrder = MemoryOrder.SEQ_CST) -> int:
        return self._impl_bin_arithmetic(OpType.FETCH_ADD, value, order)

    def fetch_sub(self, value: int, order: MemoryOrder = MemoryOrder.SEQ_CST) -> int:
        return self._impl_bin_arithmetic(OpType.FETCH_SUB, value, order)

    def fetch_inc(self, order: MemoryOrder = MemoryOrder.SEQ_CST) -> int:
        return self._impl_bin_arithmetic(OpType.FETCH_INC, None, order)

    def fetch_dec(self, order: MemoryOrder = MemoryOrder.SEQ_CST) -> int:
        return self._impl_bin_arithmetic(OpType.FETCH_DEC, None, order)

    def fetch_neg(self, order: MemoryOrder = MemoryOrder.SEQ_CST) -> int:
        return self._impl_bin_arithmetic(OpType.FETCH_NEG, None, order)
