# Exercise stencil. Klein, "Coding the Matrix", Ch. 2-3 (The Vector Space).
# Fill each function body. Verify with: python -m doctest -v vec.py
# Don't peek at solutions before attempting — the point is building the mental model
# PyTorch tensors hide behind __add__/__mul__/broadcasting.


def getitem(v, k):
    """
    Return the value of entry k in v.
    Be sure getitem(v,k) returns 0 if k is not represented in v.f.

    >>> v = Vec({'a','b','c', 'd'},{'a':2,'c':1,'d':3})
    >>> v['d']
    3
    >>> v['b']
    0
    """
    return v.f.get(k, 0)


def setitem(v, k, val):
    """
    Set the element of v with label k to be val.
    setitem(v,k,val) should set the value for key k even if k
    is not previously represented in v.f.

    >>> v = Vec({'a', 'b', 'c'}, {'b':0})
    >>> v['b'] = 5
    >>> v['b']
    5
    >>> v['a'] = 1
    >>> v['a']
    1
    """
    v.f[k] = val


def equal(u, v):
    """
    Return true iff u is equal to v.
    Because of sparse representation, it is not enough to compare dictionaries.
    Check equality for every key in u.D (== v.D), not just keys present in f.

    >>> Vec({'a', 'b', 'c'}, {'a':0}) == Vec({'a', 'b', 'c'}, {'b':0})
    True
    >>> Vec({'x','y','z'},{'y':1,'x':2}) == Vec({'x','y','z'},{'y':1,'z':0})
    False
    """
    assert u.D == v.D
    return all(getitem(u, k) == getitem(v, k) for k in u.D)


def add(u, v):
    """
    Returns the sum of the two vectors. Domains must match.

    >>> a = Vec({'a','e','i','o','u'}, {'a':0,'e':1,'i':2})
    >>> b = Vec({'a','e','i','o','u'}, {'o':4,'u':7})
    >>> c = Vec({'a','e','i','o','u'}, {'a':0,'e':1,'i':2,'o':4,'u':7})
    >>> a + b == c
    True
    """
    assert u.D == v.D
    return Vec(u.D, {k: getitem(u, k) + getitem(v, k) for k in u.D})


def dot(u, v):
    """
    Returns the dot product of the two vectors.

    >>> u1 = Vec({'a','b'}, {'a':1, 'b':2})
    >>> u2 = Vec({'a','b'}, {'b':2, 'a':1})
    >>> u1*u2
    5
    """
    assert u.D == v.D
    return sum(getitem(u, k) * getitem(v, k) for k in u.D)


def scalar_mul(v, alpha):
    """
    Returns the scalar-vector product alpha times v.

    TODO: remove the "# doctest: +SKIP" markers below once implemented.

    >>> zero = Vec({'x','y','z','w'}, {})
    >>> u = Vec({'x','y','z','w'},{'x':1,'y':2,'z':3,'w':4})
    >>> 0*u == zero  # doctest: +SKIP
    True
    >>> 0.5*u == Vec({'x','y','z','w'},{'x':0.5,'y':1,'z':1.5,'w':2})  # doctest: +SKIP
    True
    """
    raise NotImplementedError


def neg(v):
    """
    Returns the negation of a vector.

    TODO: remove the "# doctest: +SKIP" marker below once implemented.

    >>> -Vec({'a','b','c'}, {'a':1}) == Vec({'a','b','c'}, {'a':-1})  # doctest: +SKIP
    True
    """
    raise NotImplementedError


###############################################################################


class Vec:
    """
    A vector has two fields:
    D - the domain (a set)
    f - a dictionary mapping (some) domain elements to field elements;
        elements of D not appearing in f are implicitly mapped to zero.
    """

    def __init__(self, labels, function):
        self.D = labels
        self.f = function

    __getitem__ = getitem
    __setitem__ = setitem
    __neg__ = neg
    __rmul__ = scalar_mul  # if left arg of * is primitive, assume it's a scalar

    def __mul__(self, other):
        if isinstance(other, Vec):
            return dot(self, other)
        return NotImplemented  # falls back to other.__rmul__(self)

    def __truediv__(self, other):
        return (1 / other) * self

    __add__ = add

    def __radd__(self, other):
        if other == 0:
            return self

    def __sub__(a, b):
        return a + (-b)

    __eq__ = equal

    def __repr__(self):
        return "Vec(" + str(self.D) + "," + str(self.f) + ")"

    def copy(self):
        return Vec(self.D, self.f.copy())
