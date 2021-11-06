from .byteops import ByteOperationsMixin
from .intops import IntegralOperationsMixin
from .properties import BasePropertiesMixin, BytePropertiesMixin, IntegralPropertiesMixin


class ANY(BasePropertiesMixin):
    pass


class INTEGRAL(ANY, IntegralOperationsMixin, IntegralPropertiesMixin):
    pass


class BYTES(ANY, ByteOperationsMixin, BytePropertiesMixin):
    pass


class INT(INTEGRAL):
    pass


class UINT(INTEGRAL):
    pass
