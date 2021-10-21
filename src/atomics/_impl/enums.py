import enum


class MemoryOrder(enum.IntEnum):

    RELAXED = 0
    # CONSUME = 1
    ACQUIRE = 2
    RELEASE = 3
    ACQ_REL = 4
    SEQ_CST = 5

    _ignore_ = ["_BAD_LOAD_ORDERS", "_BAD_STORE_ORDERS"]
    _BAD_STORE_ORDERS: (int,) = (ACQUIRE, ACQ_REL)  # ,CONSUME
    _BAD_LOAD_ORDERS: (int,) = (RELEASE, ACQ_REL)

    def is_valid_store_order(self) -> bool:
        return self.value not in MemoryOrder._BAD_STORE_ORDERS

    def is_valid_load_order(self) -> bool:
        return self.value not in MemoryOrder._BAD_LOAD_ORDERS

    def is_valid_fail_order(self, succ: "MemoryOrder") -> bool:
        return (self.value <= succ.value) and self.is_valid_load_order()


class OpType(enum.IntEnum):

    # base
    LOAD = enum.auto()
    STORE = enum.auto()

    # xchg
    EXCHANGE = enum.auto()
    CMPXCHG_WEAK = enum.auto()
    CMPXCHG_STRONG = enum.auto()

    # bit-wise
    BIT_TEST = enum.auto()
    BIT_TEST_COMP = enum.auto()
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
