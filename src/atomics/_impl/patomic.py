from ctypes import *
import pathlib


_opsig_explicit_store_t = CFUNCTYPE(None, c_void_p, c_void_p, c_int)
_opsig_explicit_load_t = CFUNCTYPE(None, c_void_p, c_int, c_void_p)
_opsig_explicit_exchange_t = CFUNCTYPE(None, c_void_p, c_void_p, c_int, c_void_p)
_opsig_explicit_cmpxchg_t = CFUNCTYPE(c_int, c_void_p, c_void_p, c_void_p, c_int, c_int)
_opsig_explicit_test_t = CFUNCTYPE(c_int, c_void_p, c_int, c_int)
_opsig_explicit_test_modify_t = CFUNCTYPE(c_int, c_void_p, c_int, c_int)
_opsig_explicit_fetch_t = CFUNCTYPE(None, c_void_p, c_void_p, c_int, c_void_p)
_opsig_explicit_fetch_noarg_t = CFUNCTYPE(None, c_void_p, c_int, c_void_p)
_opsig_explicit_void_t = CFUNCTYPE(None, c_void_p, c_void_p, c_int)
_opsig_explicit_void_noarg_t = CFUNCTYPE(None, c_void_p, c_int)


class _OpsExplicitArithmetic(Structure):
    _fields_ = [("fp_add", _opsig_explicit_void_t),
                ("fp_sub", _opsig_explicit_void_t),
                ("fp_inc", _opsig_explicit_void_noarg_t),
                ("fp_dec", _opsig_explicit_void_noarg_t),
                ("fp_neg", _opsig_explicit_void_noarg_t),
                ("fp_fetch_add", _opsig_explicit_fetch_t),
                ("fp_fetch_sub", _opsig_explicit_fetch_t),
                ("fp_fetch_inc", _opsig_explicit_fetch_noarg_t),
                ("fp_fetch_dec", _opsig_explicit_fetch_noarg_t),
                ("fp_fetch_neg", _opsig_explicit_fetch_noarg_t)]


class _OpsExplicitBinary(Structure):
    _fields_ = [("fp_or", _opsig_explicit_void_t),
                ("fp_xor", _opsig_explicit_void_t),
                ("fp_and", _opsig_explicit_void_t),
                ("fp_not", _opsig_explicit_void_noarg_t),
                ("fp_fetch_or", _opsig_explicit_fetch_t),
                ("fp_fetch_xor", _opsig_explicit_fetch_t),
                ("fp_fetch_and", _opsig_explicit_fetch_t),
                ("fp_fetch_not", _opsig_explicit_fetch_noarg_t)]


class _OpsExplicitBitwise(Structure):
    _fields_ = [("fp_test", _opsig_explicit_test_t),
                ("fp_test_comp", _opsig_explicit_test_modify_t),
                ("fp_test_set", _opsig_explicit_test_modify_t),
                ("fp_test_reset", _opsig_explicit_test_modify_t)]


class _OpsExplicitXchg(Structure):
    _fields_ = [("fp_exchange", _opsig_explicit_exchange_t),
                ("fp_cmpxchg_weak", _opsig_explicit_cmpxchg_t),
                ("fp_cmpxchg_strong", _opsig_explicit_cmpxchg_t)]


class Ops(Structure):
    _fields_ = [("fp_store", _opsig_explicit_store_t),
                ("fp_load", _opsig_explicit_load_t),
                ("xchg_ops", _OpsExplicitXchg),
                ("bitwise_ops", _OpsExplicitBitwise),
                ("binary_ops", _OpsExplicitBinary),
                ("signed_ops", _OpsExplicitArithmetic),
                ("unsigned_ops", _OpsExplicitArithmetic)]


class Alignment(Structure):
    _fields_ = [("recommended", c_size_t),
                ("minimum", c_size_t),
                ("size_within", c_size_t)]


class Patomic:

    class _PatomicExplicit(Structure):
        _fields_ = [("ops", Ops),
                    ("align", Alignment)]

    def __init__(self):
        # get lib path
        path = pathlib.Path(__file__).parent.parent.resolve()
        path = path.joinpath("_clib")
        possible_paths = sorted(path.glob("*patomic*"))
        if not possible_paths:
            raise FileNotFoundError("Could not find libpatomic in atomics._clib")
        path = possible_paths[-1]
        # setup lib
        self._lib = cdll.LoadLibrary(str(path))
        self._lib.patomic_create_explicit.restype = Patomic._PatomicExplicit
        self._lib.patomic_create_explicit.argtypes = [c_size_t, c_int, c_int]
        self._lib.patomic_nonnull_ops_count_explicit.restype = c_int
        self._lib.patomic_nonnull_ops_count_explicit.argtypes = [POINTER(Ops)]

    def _create_explicit(self, width: int) -> _PatomicExplicit:
        char_bit = 8
        if width < 0:
            raise ValueError("Negative width")
        elif width.bit_length() > (sizeof(c_size_t) * char_bit):
            raise OverflowError(width, "Value would overflow size_t")
        return self._lib.patomic_create_explicit(width, 0, 0)

    def ops(self, width: int) -> Ops:
        pae = self._create_explicit(width)
        return pae.ops

    def alignment(self, width: int) -> Alignment:
        pae = self._create_explicit(width)
        return pae.align

    def count_nonnull_ops(self, ops: Ops, *, readonly: bool) -> int:
        res = 0
        if readonly:
            # only current non-modifying ops
            res += bool(ops.fp_load)
            res += bool(ops.bitwise_ops.fp_test)
        else:
            res = self._lib.patomic_nonnull_ops_count_explicit(byref(ops))
        return res
