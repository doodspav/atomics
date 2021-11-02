import functools


def unmoved(func):

    @functools.wraps(func)
    def _unmoved(*args, **kwargs):
        self = args[0]
        if not self._moved:
            return func(args, kwargs)
        else:
            msg = f"Operation forbidden on moved {self.__class__.__name__} object."
            raise ValueError(msg)

    return _unmoved


def unreleased(func):

    @functools.wraps(func)
    def _unreleased(*args, **kwargs):
        self = args[0]
        if not self._released:
            return func(args, kwargs)
        else:
            msg = f"Operation forbidden on released {self.__class__.__name__} object."
            raise ValueError(msg)
