# Exercise stencil. Klein, "Coding the Matrix", Ch. 4-6 (Matrices).
# Fill each function body, then remove its "# doctest: +SKIP" markers so the
# doctest actually verifies the implementation. Verify with: uv run pytest
# A Mat is a linear map: D = (row_labels, col_labels), f: (row,col) -> value.
from itertools import permutations

from coding_the_matrix.vec import Vec


def getitem(M, k):
    """
    Returns the value of entry k in M, where k is a 2-tuple.

    TODO: remove the "# doctest: +SKIP" markers below once implemented.

    >>> M = Mat(({1,3,5}, {'a'}), {(1,'a'):4, (5,'a'): 2})
    >>> M[1,'a']
    4
    >>> M[3,'a']
    0
    """
    return M.f.get(k, 0)


def setitem(M, k, val):
    """
    Set entry k of Mat M to val, where k is a 2-tuple.

    TODO: remove the "# doctest: +SKIP" markers below once implemented.

    >>> M = Mat(({'a','b','c'}, {5}), {('a', 5):3, ('b', 5):7})
    >>> M['b', 5] = 9
    >>> M['c', 5] = 13
    >>> M == Mat(({'a','b','c'}, {5}), {('a', 5):3, ('b', 5):9, ('c',5):13})
    True
    """
    M.f[k] = val


def equal(A, B):
    """
    Returns true iff A is equal to B.

    TODO: remove the "# doctest: +SKIP" marker below once implemented.

    >>> A = Mat(({'a','b'}, {0,1}), {('a',1):2, ('b',0):1})
    >>> B = Mat(({'a','b'}, {0,1}), {('a',1):2, ('b',0):1, ('b',1):0})
    >>> A == B
    True
    """
    assert A.D == B.D
    return all(getitem(A, (r, c)) == getitem(B, (r, c)) for r in A.D[0] for c in A.D[1])


def add(A, B):
    """
    Return the sum of Mats A and B. Domains must match.

    TODO: remove the "# doctest: +SKIP" marker below once implemented.

    >>> A1 = Mat(({3, 6}, {'x','y'}), {(3,'x'):-2, (6,'y'):3})
    >>> A2 = Mat(({3, 6}, {'x','y'}), {(3,'y'):4})
    >>> B = Mat(({3, 6}, {'x','y'}), {(3,'x'):-2, (3,'y'):4, (6,'y'):3})
    >>> A1 + A2 == B
    True
    """
    assert A.D == B.D
    return Mat(A.D, {(r, c): getitem(A, (r, c)) + getitem(B, (r, c))
                      for r in A.D[0] for c in A.D[1]})


def scalar_mul(M, x):
    """
    Returns the result of scaling M by x.

    TODO: remove the "# doctest: +SKIP" markers below once implemented.

    >>> M = Mat(({1,3,5}, {2,4}), {(1,2):4, (5,4):2, (3,4):3})
    >>> 1*M == M
    True
    >>> 0.25*M == Mat(({1,3,5}, {2,4}), {(1,2):1.0, (5,4):0.5, (3,4):0.75})
    True
    """
    return Mat(M.D, {(r, c): x * getitem(M, (r, c)) for r in M.D[0] for c in M.D[1]})


def transpose(M):
    """
    Returns the matrix that is the transpose of M.

    TODO: remove the "# doctest: +SKIP" marker below once implemented.

    >>> M = Mat(({0,1}, {0,1}), {(0,1):3, (1,0):2, (1,1):4})
    >>> M.transpose() == Mat(({0,1}, {0,1}), {(0,1):2, (1,0):3, (1,1):4})
    True
    """
    return Mat((M.D[1], M.D[0]), {(c, r): val for (r, c), val in M.f.items()})


def vector_matrix_mul(v, M):
    """
    Returns the product of vector v and matrix M (v as a row vector).

    TODO: remove the "# doctest: +SKIP" marker below once implemented.

    >>> v1 = Vec({1, 2, 3}, {1: 1, 2: 8})
    >>> M1 = Mat(({1, 2, 3}, {'a', 'b', 'c'}), {(1, 'b'): 2, (2, 'a'):-1, (3, 'a'): 1, (3, 'c'): 7})
    >>> v1*M1 == Vec({'a', 'b', 'c'},{'a': -8, 'b': 2, 'c': 0})
    True
    """
    assert v.D == M.D[0]
    return Vec(M.D[1], {c: sum(v[r] * M[r, c] for r in M.D[0]) for c in M.D[1]})


def matrix_vector_mul(M, v):
    """
    Returns the product of matrix M and vector v (v as a column vector).

    TODO: remove the "# doctest: +SKIP" marker below once implemented.

    >>> N1 = Mat(({1, 3, 5, 7}, {'a', 'b'}), {(1, 'a'): -1, (1, 'b'): 2, (3, 'a'): 1, (3, 'b'):4, (7, 'a'): 3, (5, 'b'):-1})
    >>> u1 = Vec({'a', 'b'}, {'a': 1, 'b': 2})
    >>> N1*u1 == Vec({1, 3, 5, 7},{1: 3, 3: 9, 5: -2, 7: 3})
    True
    """
    assert v.D == M.D[1]
    return Vec(M.D[0], {r: sum(M[r, c] * v[c] for c in M.D[1]) for r in M.D[0]})


def matrix_matrix_mul(A, B):
    """
    Returns the result of the matrix-matrix multiplication, A*B.

    TODO: remove the "# doctest: +SKIP" marker below once implemented.

    >>> A = Mat(({0,1,2}, {0,1,2}), {(1,1):4, (0,0):0, (1,2):1, (1,0):5, (0,1):3, (0,2):2})
    >>> B = Mat(({0,1,2}, {0,1,2}), {(1,0):5, (2,1):3, (1,1):2, (2,0):0, (0,0):1, (0,1):4})
    >>> A*B == Mat(({0,1,2}, {0,1,2}), {(0,0):15, (0,1):12, (1,0):25, (1,1):31})
    True
    """
    assert A.D[1] == B.D[0]
    return Mat((A.D[0], B.D[1]),
               {(r, c): sum(A[r, k] * B[k, c] for k in A.D[1]) for r in A.D[0] for c in B.D[1]})


def identity(D):
    """
    Returns the DxD identity matrix over domain D.

    >>> identity({0,1,2}) == Mat(({0,1,2},{0,1,2}), {(0,0):1,(1,1):1,(2,2):1})
    True
    """
    return Mat((D, D), {(d, d): 1 for d in D})


def mat2rowdict(M):
    """
    Returns a dict mapping each row label of M to the Vec representing that row.

    >>> M = Mat(({'a','b'}, {'#','@'}), {('a','#'):1, ('a','@'):2, ('b','#'):10, ('b','@'):20})
    >>> mat2rowdict(M) == {'a': Vec({'#','@'}, {'#':1,'@':2}), 'b': Vec({'#','@'}, {'#':10,'@':20})}
    True
    """
    return {r: Vec(M.D[1], {c: M[r, c] for c in M.D[1]}) for r in M.D[0]}


def mat2coldict(M):
    """
    Returns a dict mapping each column label of M to the Vec representing that column.

    >>> M = Mat(({'a','b'}, {'#','@'}), {('a','#'):1, ('a','@'):2, ('b','#'):10, ('b','@'):20})
    >>> mat2coldict(M) == {'#': Vec({'a','b'}, {'a':1,'b':10}), '@': Vec({'a','b'}, {'a':2,'b':20})}
    True
    """
    return {c: Vec(M.D[0], {r: M[r, c] for r in M.D[0]}) for c in M.D[1]}


def _table(M, row_labels, col_labels):
    """Shared table-builder for to_str/pp: same formatting, caller picks row/col order."""
    col_w = max([len(str(c)) for c in col_labels]
                + [len(str(M[r, c])) for r in row_labels for c in col_labels] + [1])
    row_w = max([len(str(r)) for r in row_labels] + [1])
    header = ' ' * row_w + ' ' + ' '.join(str(c).rjust(col_w) for c in col_labels)
    sep = '-' * len(header)
    lines = [header, sep]
    for r in row_labels:
        vals = ' '.join(str(M[r, c]).rjust(col_w) for c in col_labels)
        lines.append(str(r).rjust(row_w) + ' ' + vals)
    return '\n'.join(lines)


def to_str(M):
    """
    Returns the book-style pretty-printed table for Mat M: a header row of
    column labels, a separator, then one row per row-label with its values —
    everything right-justified to the widest entry in its column. Row/column
    order is alphabetical; for a chosen order (Klein 4.6.10/4.6.11), use pp().

    >>> print(Mat(({'a','b'}, {'x','y'}), {('a','x'):1, ('a','y'):2, ('b','x'):10, ('b','y'):20}))
       x  y
    -------
    a  1  2
    b 10 20
    """
    return _table(M, sorted(M.D[0], key=str), sorted(M.D[1], key=str))


def pp(M, L_R, L_C):
    """
    Pretty-prints M with rows ordered by L_R and columns ordered by L_C
    (Klein 4.6.10/4.6.11) instead of __str__'s fixed alphabetical order —
    lets you reveal triangular structure that's hidden under the default order.

    >>> A = Mat(({'a','b','c'}, {'#','@','?'}),
    ...         {('a','#'):2, ('a','?'):3,
    ...          ('b','@'):10, ('b','#'):20, ('b','?'):30,
    ...          ('c','#'):35})
    >>> print(A.pp(['b','a','c'], ['@','?','#']))
       @  ?  #
    ----------
    b 10 30 20
    a  0  3  2
    c  0  0 35
    """
    return _table(M, L_R, L_C)


def find_triangular_order(M):
    """
    Problem 4.6.12: find a row-label list L_R and column-label list L_C with
    respect to which M is triangular (M[L_R[i], L_C[j]] == 0 for i > j), or
    return None if no such lists exist. Only defined for square M (same
    number of row and column labels) — that's required for i>j to line up
    row-for-row with column-for-column.

    Brute-force over all row/column permutations — O(n!^2), fine for the
    small hand-worked matrices in the book. The book hints at a real
    graph-algorithm (topological sort on the row/column dependency graph)
    for matrices too large to permute exhaustively; not implemented here.

    >>> A = Mat(({'a','b','c'}, {'#','@','?'}),
    ...         {('a','#'):2, ('a','?'):3,
    ...          ('b','@'):10, ('b','#'):20, ('b','?'):30,
    ...          ('c','#'):35})
    >>> L_R, L_C = find_triangular_order(A)
    >>> all(A[L_R[i], L_C[j]] == 0 for i in range(3) for j in range(3) if i > j)
    True
    """
    rows, cols = list(M.D[0]), list(M.D[1])
    if len(rows) != len(cols):
        return None
    n = len(rows)
    for L_R in permutations(rows):
        for L_C in permutations(cols):
            if all(M[L_R[i], L_C[j]] == 0 for i in range(n) for j in range(n) if i > j):
                return list(L_R), list(L_C)
    return None


###############################################################################


class Mat:
    def __init__(self, labels, function):
        self.D = labels
        self.f = function

    __getitem__ = getitem
    __setitem__ = setitem
    transpose = transpose
    mat2rowdict = mat2rowdict
    mat2coldict = mat2coldict
    pp = pp

    def __neg__(self):
        return (-1) * self

    def __mul__(self, other):
        if isinstance(other, Mat):
            return matrix_matrix_mul(self, other)
        elif isinstance(other, Vec):
            return matrix_vector_mul(self, other)
        else:
            return scalar_mul(self, other)

    def __rmul__(self, other):
        if isinstance(other, Vec):
            return vector_matrix_mul(other, self)
        return scalar_mul(self, other)

    __add__ = add

    def __radd__(self, other):
        if other == 0:
            return self

    def __sub__(a, b):
        return a + (-b)

    __eq__ = equal

    def copy(self):
        return Mat(self.D, self.f.copy())

    def __repr__(self):
        return "Mat(" + str(self.D) + ", " + str(self.f) + ")"

    __str__ = to_str
