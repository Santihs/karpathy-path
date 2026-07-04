# Klein, "Coding the Matrix", Sec. 2.11 — solving triangular systems by backward substitution.
#
# A triangular system: row i has zeros in the first i "pivot" positions, so row i
# involves only the unknown x_i and unknowns already solved by later rows.
# Solve from the LAST row up: each row has exactly one new unknown, isolate it
# with a dot-product against the partially-built solution vector x, divide by
# the pivot (row[i][i]). This is the linear-algebra core of solving Ax=b without
# a generic (expensive) inverse — same idea LU decomposition + back-substitution
# uses inside numpy.linalg.solve / torch.linalg.solve for real systems.
from coding_the_matrix.vecutil import zero_vec


def triangular_solve_n(rowlist, b):
    """
    Solve a triangular system whose rows all have domain {0, 1, ..., n-1}.

    input: rowlist, a list of n Vecs (domain {0,...,n-1}) with rowlist[i][i] != 0;
           b, a length-n list of numbers.
    output: Vec x such that rowlist[i] * x == b[i] for every i.

    >>> from coding_the_matrix.vec import Vec
    >>> rowlist = [
    ...     Vec({0,1,2,3}, {0:1, 1:0.5, 2:-2, 3:4}),
    ...     Vec({0,1,2,3}, {1:3, 2:3, 3:2}),
    ...     Vec({0,1,2,3}, {2:1, 3:5}),
    ...     Vec({0,1,2,3}, {3:2}),
    ... ]
    >>> b = [-8, 3, -4, 6]
    >>> x = triangular_solve_n(rowlist, b)
    >>> [round(x[i], 6) for i in range(4)]
    [-67.0, 18.0, -19.0, 3.0]
    >>> [round(rowlist[i] * x, 6) for i in range(4)] == b
    True
    """
    D = rowlist[0].D
    n = len(D)
    assert D == set(range(n))
    x = zero_vec(D)
    for i in reversed(range(n)):
        assert rowlist[i][i] != 0, f"zero pivot at row {i} — no unique solution (Prop. 2.11.6)"
        x[i] = (b[i] - rowlist[i] * x) / rowlist[i][i]
    return x


def triangular_solve(rowlist, label_list, b):
    """
    Solve a triangular system with an arbitrary (non-integer) domain.

    label_list gives the pivot order: row i must be zero at label_list[0..i-1]
    and nonzero at label_list[i].

    >>> from coding_the_matrix.vec import Vec
    >>> label_list = ['a', 'b', 'c', 'd']
    >>> D = set(label_list)
    >>> rowlist = [
    ...     Vec(D, {'a':4, 'b':-2, 'c':0.5, 'd':1}),
    ...     Vec(D, {'b':2, 'c':3, 'd':3}),
    ...     Vec(D, {'c':5, 'd':1}),
    ...     Vec(D, {'d':2.}),
    ... ]
    >>> b = [6, -4, 3, -8]
    >>> x = triangular_solve(rowlist, label_list, b)
    >>> [round(x[c], 3) for c in label_list]
    [3.275, 1.9, 1.4, -4.0]
    """
    D = rowlist[0].D
    x = zero_vec(D)
    for j in reversed(range(len(D))):
        c = label_list[j]
        row = rowlist[j]
        assert row[c] != 0, f"zero pivot at row {j} (label {c!r}) — no unique solution (Prop. 2.11.6)"
        x[c] = (b[j] - x * row) / row[c]
    return x
