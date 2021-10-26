from ..alignment import Alignment
from ..enums import MemoryOrder, OpType
from ..exceptions import AlignmentError, MemoryOrderError, UnsupportedWidthException, UnsupportedOperationException
from ..patomic import Patomic
from ..pybuffer import PyBuffer

from typing import Callable, Dict, Optional, Tuple


class AtomicBase:

    def __init__(self, buffer_or_width, *, is_integral: bool, is_signed: bool):
        # check if object has been initialised
        if hasattr(self, "_buffer"):
            raise ValueError("Atomic object cannot be re-initialised.")
        self._is_integral: bool = is_integral
        self._is_signed: bool = is_signed
        # get buffer
        error_msg = None
        try:
            # parse as buffer
            with memoryview(buffer_or_width) as view:
                self._buffer = PyBuffer(buffer_or_width, writeable=(not view.readonly))
        except TypeError:
            # parse as width
            if isinstance(buffer_or_width, int):
                self._buffer = PyBuffer(bytearray(buffer_or_width), writeable=True)
            # incompatible type
            else:
                error_msg = "Positional argument 'buffer_or_width' must either support the " \
                            "buffer protocol, or have type 'int'."
        if error_msg:
            raise TypeError(error_msg)
        # check ops are available
        width = len(self._buffer)
        p = Patomic()
        self._ops = p.ops(width)
        if p.count_nonnull_ops(self._ops, readonly=self.readonly) == 0:
            raise UnsupportedWidthException(width, readonly=self.readonly)
        # check buffer meets alignment requirements
        align = Alignment(width)
        if not align.is_valid_recommended(self._buffer.address):
            raise AlignmentError(width, self._buffer.address, using_recommended=True)
        # cache supported ops
        self._supported: Dict[OpType, Callable] = self._get_supported_ops_map()

    def _get_supported_ops_map(self) -> Dict[OpType, Callable]:
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
        return ots

    @staticmethod
    def _require_int_type(width) -> None:
        if type(width) is not int:
            error_msg = "Positional argument 'width' must have type 'int'."
            raise TypeError(error_msg)

    @staticmethod
    def _require_buffer_protocol(buffer) -> None:
        try:
            with memoryview(buffer):
                return
        except TypeError:
            error_msg = "Positional argument 'buffer' must support the buffer protocol."
        raise TypeError(error_msg)

    @property
    def _address(self) -> int:
        return self._buffer.address

    @property
    def width(self) -> int:
        return len(self._buffer)

    @property
    def readonly(self) -> bool:
        return self._buffer.readonly

    @property
    def ops_supported(self) -> [OpType]:
        return sorted(list(self._supported.keys()))

    def store(self, desired: bytes, order: MemoryOrder = MemoryOrder.SEQ_CST) -> None:
        # check support
        fp = self._supported.get(OpType.STORE)
        if fp is None:
            raise UnsupportedOperationException(OpType.STORE, self.width, readonly=self.readonly)
        # validate inputs
        elif not order.is_valid_store_order():
            raise MemoryOrderError(OpType.STORE, order, is_fail=False)
        elif len(desired) != self.width:
            raise ValueError("'desired' bytes object length does not match width")
        # perform operation
        des_buf = PyBuffer(desired, writeable=False)
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
        res_buf = PyBuffer(result, writeable=True, force=True)
        # modifying result contents directly is fine (no impl will place it in RO memory)
        fp(self._address, order.value, res_buf.address)
        return result

    def exchange(self, desired: bytes, order: MemoryOrder = MemoryOrder.SEQ_CST) -> bytes:
        # check support
        fp = self._supported.get(OpType.EXCHANGE)
        if fp is None:
            raise UnsupportedOperationException(OpType.EXCHANGE, self.width, readonly=self.readonly)
        # validate input
        elif len(desired) != self.width:
            raise ValueError("'desired' bytes object length does not match width")
        # perform operation
        result = bytes(self.width)
        res_buf = PyBuffer(result, writeable=True, force=True)
        # modifying result contents directly is fine (no impl will place it in RO memory)
        des_buf = PyBuffer(desired, writeable=False)
        fp(self._address, des_buf.address, order.value, res_buf.address)
        return result

    def _impl_cmpxchg(self, optype: OpType, expected: bytes, desired: bytes,
                      succ: MemoryOrder, fail: MemoryOrder) -> Tuple[bool, bytes]:
        assert("CMPXCHG" in optype.name)
        # check support
        fp = self._supported.get(optype)
        if fp is None:
            raise UnsupportedOperationException(optype, self.width, readonly=self.readonly)
        # validate inputs
        elif len(expected) != self.width:
            raise ValueError("'expected' bytes object length does not match width")
        elif len(desired) != self.width:
            raise ValueError("'desired' bytes object length does not match width")
        elif not fail.is_valid_fail_order(succ):
            raise MemoryOrderError(optype, fail, is_fail=True)
        # perform operation
        exp_mut = bytes(expected)  # make a copy so we can modify it
        exp_buf = PyBuffer(exp_mut, writeable=True, force=True)
        des_mut = bytes(desired)  # make a copy so we can modify it
        des_buf = PyBuffer(des_mut, writeable=True, force=True)
        # modifying exp and des contents directly is fine (no impl will place it in RO memory)
        ok = fp(self._address, exp_buf.address, des_buf.address, succ.value, fail.value)
        return bool(ok), exp_mut

    def _impl_bit_test(self, optype: OpType, index: int, order: MemoryOrder) -> bool:
        assert("BIT_TEST" in optype.name)
        # check support
        fp = self._supported.get(optype)
        if fp is None:
            raise UnsupportedOperationException(optype, self.width, readonly=self.readonly)
        # validate input
        elif index < 0 or index > (self.width * 8):  # CHAR_BIT == 8
            raise ValueError("'index' value out of range")
        # perform operation
        return bool(fp(self._address, index, order.value))

    def _impl_bin_ari(self, optype: OpType, value: Optional[bytes],
                      order: MemoryOrder) -> Optional[bytes]:
        assert(optype.value >= OpType.OR.value)
        # check support
        fp = self._supported.get(optype)
        if fp is None:
            raise UnsupportedOperationException(optype, self.width, readonly=self.readonly)
        # validate input
        elif value is not None and len(value) != self.width:
            raise ValueError("'value' bytes object length does not match width")
        # setup args list
        args = [self._address]
        val_buf = None
        if value is not None:
            val_buf = PyBuffer(value, writeable=False)
            args.append(val_buf.address)
        args.append(order.value)
        result = None
        res_buf = None
        if "FETCH" in optype.name:
            result = bytes(self.width)
            res_buf = PyBuffer(result, writeable=True, force=True)
            # modifying result contents directly is fine (no impl will place it in RO memory)
            args.append(res_buf.address)
        # perform operation
        fp(*args)
        return result
