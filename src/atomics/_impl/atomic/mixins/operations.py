from ...enums import MemoryOrder, OpType
from ...exceptions import MemoryOrderError, UnsupportedOperationException
from ...pybuffer import PyBuffer

import sys
from typing import Callable, Dict, Optional, Tuple


class _ImplOperationsMixin:

    _address: int
    _supported: Dict[OpType, Callable]

    width: int
    readonly: bool

    def _impl_cmpxchg(self, optype: OpType, expected: bytes, desired: bytes,
                      succ: MemoryOrder, fail: MemoryOrder) -> Tuple[bool, bytes]:
        assert ("CMPXCHG" in optype.name)
        # check support
        fp = self._supported.get(optype)
        if fp is None:
            raise UnsupportedOperationException(optype, self.width, readonly=self.readonly)
        # validate inputs
        elif len(expected) != self.width:
            raise ValueError("'expected' length does not match width.")
        elif len(desired) != self.width:
            raise ValueError("'desired' length does not match width.")
        elif not fail.is_valid_fail_order(succ):
            raise MemoryOrderError(optype, fail, is_fail=True)
        # perform operation
        exp_mut = bytes(expected)  # make a copy so we can modify it
        des_mut = bytes(desired)  # make a copy so we can modify it
        with PyBuffer(exp_mut, writeable=True, force=True) as exp_buf:
            with PyBuffer(des_mut, writeable=True, force=True) as des_buf:
                # modifying exp and des contents directly is fine in this case
                ok = fp(self._address, exp_buf.address, des_buf.address, succ.value, fail.value)
        return bool(ok), exp_mut

    def _impl_bit_test(self, optype: OpType, index: int, order: MemoryOrder) -> bool:
        assert ("BIT_TEST" in optype.name)
        # check support
        fp = self._supported.get(optype)
        if fp is None:
            raise UnsupportedOperationException(optype, self.width, readonly=self.readonly)
        # validate input
        elif index < 0 or index >= (self.width * 8):  # CHAR_BIT == 8
            raise ValueError("'index' value out of range.")
        # perform operation
        return bool(fp(self._address, index, order.value))

    def _impl_bin_ari(self, optype: OpType, value: Optional[bytes],
                      order: MemoryOrder) -> Optional[bytes]:
        assert (optype.value >= OpType.OR.value)
        # check support
        fp = self._supported.get(optype)
        if fp is None:
            raise UnsupportedOperationException(optype, self.width, readonly=self.readonly)
        # validate input
        elif value is not None and len(value) != self.width:
            raise ValueError("'value' length does not match width.")
        # setup args list
        args = [self._address]
        bufs = []
        # value param
        if value is not None:
            val_buf = PyBuffer(value, writeable=False)
            args.append(val_buf.address)
            bufs.append(val_buf)
        # memory order param
        args.append(order.value)
        # result "param"
        result = None
        if "FETCH" in optype.name:
            result = bytes(self.width)
            res_buf = PyBuffer(result, writeable=True, force=True)
            # modifying result contents directly is fine in this case
            args.append(res_buf.address)
            bufs.append(res_buf)
        # perform operation
        fp(*args)
        # release buffers and return
        for buf in bufs:
            buf.release()
        return result


class ByteOperationsMixin(_ImplOperationsMixin):

    def store(self, desired: bytes, order: MemoryOrder = MemoryOrder.SEQ_CST) -> None:
        # check support
        fp = self._supported.get(OpType.STORE)
        if fp is None:
            raise UnsupportedOperationException(OpType.STORE, self.width, readonly=self.readonly)
        # validate inputs
        elif not order.is_valid_store_order():
            raise MemoryOrderError(OpType.STORE, order, is_fail=False)
        elif len(desired) != self.width:
            raise ValueError("'desired' length does not match width.")
        # perform operation
        with PyBuffer(desired, writeable=False) as des_buf:
            fp(self._address, des_buf.address, order.value)

    def load(self, order: MemoryOrder = MemoryOrder.SEQ_CST) -> bytes:
        # check support
        fp = self._supported.get(OpType.LOAD)
        if fp is None:
            raise UnsupportedOperationException(OpType.LOAD, self.width, readonly=self.readonly)
        # validate input
        elif not order.is_valid_load_order():
            raise MemoryOrderError(OpType.LOAD, order, is_fail=False)
        # perform operation
        result = bytes(self.width)
        with PyBuffer(result, writeable=True, force=True) as res_buf:
            # modifying result contents directly is fine in this case
            fp(self._address, order.value, res_buf.address)
        return result

    def exchange(self, desired: bytes, order: MemoryOrder = MemoryOrder.SEQ_CST) -> bytes:
        # check support
        fp = self._supported.get(OpType.EXCHANGE)
        if fp is None:
            raise UnsupportedOperationException(OpType.EXCHANGE, self.width, readonly=self.readonly)
        # validate input
        elif len(desired) != self.width:
            raise ValueError("'desired' length does not match width")
        # perform operation
        result = bytes(self.width)
        with PyBuffer(result, writeable=True, force=True) as res_buf:
            # modifying result contents is directly is fine in this case
            with PyBuffer(desired, writeable=False) as des_buf:
                fp(self._address, des_buf.address, order.value, res_buf.address)
        return result

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

    def bit_test_compl(self, index: int, order: MemoryOrder = MemoryOrder.SEQ_CST) -> bool:
        return self._impl_bit_test(OpType.BIT_TEST_COMPL, index, order)

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


class IntegralOperationsMixin(ByteOperationsMixin):

    signed: bool

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
