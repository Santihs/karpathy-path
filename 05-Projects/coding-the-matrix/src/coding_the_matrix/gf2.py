# GF(2) field element — infra, not an exercise (kept as reference implementation).
# Klein, "Coding the Matrix", Ch. 0 (The Field).
from numbers import Number


class One:
    def __add__(self, other): return self if other == 0 else 0
    __sub__ = __add__

    def __mul__(self, other):
        if isinstance(other, Number):
            return 0 if other == 0 else self
        return other

    def __truediv__(self, other):
        if other == 0:
            raise ZeroDivisionError
        return self

    __rtruediv__ = lambda self, other: other
    __radd__ = __add__
    __rsub__ = __add__
    __rmul__ = __mul__

    def __lt__(self, other): return False  # hack: not(one < x) for every x

    def __str__(self): return 'one'
    __repr__ = __str__

    def __neg__(self): return self
    def __bool__(self): return True
    def __format__(self, format_spec): return format(str(self), format_spec)


one = One()
zero = 0
