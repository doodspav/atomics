from .enums import MemoryOrder, OpType


class AlignmentError(Exception):

    def __init__(self, width: int, address: int, *, using_recommended: bool):
        self.width: int = width
        self.address: int = address
        self.using_recommended: int = using_recommended
        u_type = "recommended" if using_recommended else "minimum"
        message = f"The alignment of address {hex(address)} does not meet " \
                  f"the {u_type} alignment requirements for atomic operations " \
                  f"on objects with a width of {width}."
        super().__init__(message)


class MemoryOrderError(Exception):

    def __init__(self, optype: OpType, order: MemoryOrder, *, is_fail: bool):
        self.optype: OpType = optype
        self.order: MemoryOrder = order
        self.is_fail: bool = is_fail
        f_type = "fail " if is_fail else " "
        v_type = "an" if optype.name.lower()[0] in "aeiou" else "a"
        message = f"{order.name} is not a valid {f_type}memory order for " \
                  f"{v_type} {optype.name} operation."
        super().__init__(message)


class UnsupportedWidthException(Exception):

    def __init__(self, width: int, *, readonly: bool):
        self.width: int = width
        self.readonly: bool = readonly
        r_type = "readonly " if readonly else " "
        message = f"No operations are supported on {r_type}objects with a width " \
                  f"of {width}."
        super().__init__(message)


class UnsupportedOperationException(Exception):

    def __init__(self, optype: OpType, width: int, *, readonly: bool):
        self.optype: OpType = optype
        self.width: int = width
        self.readonly: bool = readonly
        r_type = "readonly " if readonly else " "
        message = f"Operation {optype.name} is not supported on {r_type}objects " \
                  f"with a width of {width}."
        super().__init__(message)
