import enum
from typing import Optional


class MemoryOrder(enum.IntEnum):

    RELAXED = 0
    # CONSUME = 1
    ACQUIRE = 2
    RELEASE = 3
    ACQ_REL = 4
    SEQ_CST = 5

    def is_valid_store_order(self) -> bool:
        return self.value not in (1, 2, 4)  # CONSUME, ACQUIRE, ACQ_REL

    def is_valid_load_order(self) -> bool:
        return self.value not in (3, 4)  # RELEASE, ACQ_REL

    def is_valid_fail_order(self, succ: "MemoryOrder") -> bool:
        return (self.value <= succ.value) and self.is_valid_load_order()


class OpType(enum.IntEnum):

    def __init__(self, value):
        fname: str = self.name.lower()
        # get function name
        if fname.startswith("bit"):
            fname = fname[len("bit_"):]
        fname = "fp_" + fname
        # get category name
        cname: Optional[str] = None
        if "xch" in fname:
            cname = "xchg_ops"
        elif "test" in fname:
            cname = "bitwise_ops"
        elif fname.endswith(("or", "xor", "and", "not")):
            cname = "binary_ops"
        elif fname not in ("fp_store", "fp_load"):
            cname = "arithmetic_ops"
        # assign to self
        self.fname = fname
        self.cname = cname

    # base (category=None)
    STORE = enum.auto()
    LOAD = enum.auto()

    # xchg
    EXCHANGE = enum.auto()
    CMPXCHG_WEAK = enum.auto()
    CMPXCHG_STRONG = enum.auto()

    # bit-wise
    BIT_TEST = enum.auto()
    BIT_TEST_COMPL = enum.auto()
    BIT_TEST_SET = enum.auto()
    BIT_TEST_RESET = enum.auto()

    # binary
    OR = enum.auto()
    XOR = enum.auto()
    AND = enum.auto()
    NOT = enum.auto()
    FETCH_OR = enum.auto()
    FETCH_XOR = enum.auto()
    FETCH_AND = enum.auto()
    FETCH_NOT = enum.auto()

    # arithmetic
    ADD = enum.auto()
    SUB = enum.auto()
    INC = enum.auto()
    DEC = enum.auto()
    NEG = enum.auto()
    FETCH_ADD = enum.auto()
    FETCH_SUB = enum.auto()
    FETCH_INC = enum.auto()
    FETCH_DEC = enum.auto()
    FETCH_NEG = enum.auto()
