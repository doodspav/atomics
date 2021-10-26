from .base import AtomicBase
from ..enums import MemoryOrder, OpType
from ..exceptions import MemoryOrderError

from typing import Tuple


class AtomicBytes(AtomicBase):

    def __init__(self, *, buffer_or_width):
        super().__init__(buffer_or_width, is_integral=False, is_signed=False)

    @classmethod
    def from_buffer(cls, buffer):
        cls._require_buffer_protocol(buffer)
        return cls(buffer_or_width=buffer)

    @classmethod
    def from_width(cls, width: int):
        cls._require_int_type(width)
        return cls(buffer_or_width=width)

    def cmpxchg_weak(self, expected: bytes, desired: bytes,
                     succ: MemoryOrder = MemoryOrder.SEQ_CST,
                     fail: MemoryOrder = MemoryOrder.SEQ_CST) -> Tuple[bool, bytes]:
        return self._impl_cmpxchg(OpType.CMPXCHG_WEAK, expected, desired, succ, fail)

    def cmpxchg_strong(self, expected: bytes, desired: bytes,
                       succ: MemoryOrder = MemoryOrder.SEQ_CST,
                       fail: MemoryOrder = MemoryOrder.SEQ_CST) -> Tuple[bool, bytes]:
        return self._impl_cmpxchg(OpType.CMPXCHG_STRONG, expected, desired, succ, fail)

    def bit_test(self, index: int, order: MemoryOrder = MemoryOrder.SEQ_CST) -> bool:
        if not order.is_valid_store_order():
            raise MemoryOrderError(OpType.BIT_TEST, order, is_fail=False)
        return self._impl_bit_test(OpType.BIT_TEST, index, order)

    def bit_test_comp(self, index: int, order: MemoryOrder = MemoryOrder.SEQ_CST) -> bool:
        return self._impl_bit_test(OpType.BIT_TEST_COMP, index, order)

    def bit_test_set(self, index: int, order: MemoryOrder = MemoryOrder.SEQ_CST) -> bool:
        return self._impl_bit_test(OpType.BIT_TEST_SET, index, order)

    def bit_test_reset(self, index: int, order: MemoryOrder = MemoryOrder.SEQ_CST) -> bool:
        return self._impl_bit_test(OpType.BIT_TEST_RESET, index, order)

    def bin_or(self, value: bytes, order: MemoryOrder = MemoryOrder.SEQ_CST) -> None:
        return self._impl_bin_ari(OpType.OR, value, order)

    def bin_xor(self, value: bytes, order: MemoryOrder = MemoryOrder.SEQ_CST) -> None:
        return self._impl_bin_ari(OpType.XOR, value, order)

    def bin_and(self, value: bytes, order: MemoryOrder = MemoryOrder.SEQ_CST) -> None:
        return self._impl_bin_ari(OpType.AND, value, order)

    def bin_not(self, order: MemoryOrder = MemoryOrder.SEQ_CST) -> None:
        return self._impl_bin_ari(OpType.NOT, None, order)

    def bin_fetch_or(self, value: bytes, order: MemoryOrder = MemoryOrder.SEQ_CST) -> bytes:
        return self._impl_bin_ari(OpType.FETCH_OR, value, order)

    def bin_fetch_xor(self, value: bytes, order: MemoryOrder = MemoryOrder.SEQ_CST) -> bytes:
        return self._impl_bin_ari(OpType.FETCH_XOR, value, order)

    def bin_fetch_and(self, value: bytes, order: MemoryOrder = MemoryOrder.SEQ_CST) -> bytes:
        return self._impl_bin_ari(OpType.FETCH_AND, value, order)

    def bin_fetch_not(self, order: MemoryOrder = MemoryOrder.SEQ_CST) -> bytes:
        return self._impl_bin_ari(OpType.FETCH_NOT, None, order)
