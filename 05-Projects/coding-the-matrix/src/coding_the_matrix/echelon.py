# Klein, "Coding the Matrix", Ch. 7 — Gaussian elimination.
#
# The core move: reduce a matrix to echelon form while tracking every row
# operation as a matrix M, so that M @ A == echelon_form(A). Because M is a
# product of invertible elementary row-addition matrices, M is invertible too,
# and Row(M @ A) == Row(A) (Corollary 7.1.4) — the row space never changes,
# only how it's expressed. That single invariant is what makes echelon form
# useful for three different jobs: basis for the row space, solving Ax=b,
# and basis for the null space of A^T (rows of M paired with zero rows of MA).
from coding_the_matrix.vec import Vec
from coding_the_matrix.vecutil import zero_vec


def _col_order(D):
    # sorted(D, key=hash) is what the book uses, but str hashes are randomized
    # per-process in Python 3 — that makes the column order (and therefore
    # which row becomes "the" pivot) different every run, which breaks
    # reproducible doctests/tests. key=repr is just as arbitrary but stable.
    return sorted(D, key=repr)


def _gaussian_elimination(rowlist, record=None):
    """
    Shared engine behind transformation(), echelon_form(), row_reduce(), and
    null_space_basis(). Returns (M, U), both length-m lists of Vecs, such
    that M is invertible and matrix(M) @ matrix(rowlist) == matrix(U), with
    U in echelon form (pivot rows first, in column order; zero rows last).

    record: optional list. If given, a dict snapshot is appended after every
    pivot selection and after every row-addition — visualize_gaussian.py uses
    this to animate the algorithm without duplicating its logic.
    """
    m = len(rowlist)
    D = rowlist[0].D
    rowlist = list(rowlist)  # local copy — never mutate the caller's list
    M_rowlist = [Vec(set(range(m)), {i: 1}) for i in range(m)]  # identity

    rows_left = set(range(m))
    new_rowlist = []
    new_M_rowlist = []

    for c in _col_order(D):
        rows_with_nonzero = [r for r in rows_left if rowlist[r][c] != 0]
        if not rows_with_nonzero:
            continue
        pivot = rows_with_nonzero[0]
        rows_left.remove(pivot)
        new_rowlist.append(rowlist[pivot])
        new_M_rowlist.append(M_rowlist[pivot])
        if record is not None:
            record.append({
                "kind": "pivot",
                "column": c,
                "pivot_row": pivot,
                "rowlist": list(rowlist),
            })
        for r in rows_with_nonzero[1:]:
            multiplier = rowlist[r][c] / rowlist[pivot][c]
            rowlist[r] = rowlist[r] - multiplier * rowlist[pivot]
            M_rowlist[r] = M_rowlist[r] - multiplier * M_rowlist[pivot]
            if record is not None:
                record.append({
                    "kind": "row-addition",
                    "column": c,
                    "pivot_row": pivot,
                    "target_row": r,
                    "multiplier": multiplier,
                    "rowlist": list(rowlist),
                })

    # Every row still in rows_left has, by construction, a zero in every
    # column we iterated over — it IS the zero vector. Tack them on last.
    for r in rows_left:
        new_rowlist.append(rowlist[r])
        new_M_rowlist.append(M_rowlist[r])

    return new_M_rowlist, new_rowlist


def transformation(rowlist):
    """
    Return M, a list of m Vecs (domain {0,...,m-1}), such that M is
    invertible and matrix(M) @ matrix(rowlist) is in echelon form
    (Proposition 7.3.1).

    >>> from coding_the_matrix.vecutil import list2vec
    >>> D = {0, 1, 2, 3, 4}
    >>> A = [
    ...     list2vec([0, 2, 3, 4, 5]),
    ...     list2vec([0, 0, 0, 3, 2]),
    ...     list2vec([1, 2, 3, 4, 5]),
    ...     list2vec([0, 0, 0, 6, 7]),
    ...     list2vec([0, 0, 0, 9, 8]),
    ... ]
    >>> M = transformation(A)
    >>> MA = [sum((M_row[i] * A[i] for i in range(5)), zero_vec(D)) for M_row in M]
    >>> [round(MA[r][c], 6) for r in range(5) for c in range(5)] == [
    ...     1,2,3,4,5, 0,2,3,4,5, 0,0,0,3,2, 0,0,0,0,3, 0,0,0,0,0]
    True
    """
    M, _ = _gaussian_elimination(rowlist)
    return M


def echelon_form(rowlist):
    """
    Return the matrix (as a list of m Vecs) obtained from rowlist by
    Gaussian elimination — pivot rows in column order, zero rows last.

    >>> from coding_the_matrix.vecutil import list2vec
    >>> A = [list2vec([0, 2, 3]), list2vec([1, 2, 3]), list2vec([0, 0, 6])]
    >>> U = echelon_form(A)
    >>> [[U[r][c] for c in range(3)] for r in range(3)]
    [[1, 2, 3], [0, 2, 3], [0, 0, 6]]
    """
    _, U = _gaussian_elimination(rowlist)
    return U


def row_reduce(rowlist):
    """
    Return a basis (in echelon form, no zero vectors) for the row space of
    rowlist — Lemma 7.1.2.

    >>> from coding_the_matrix.vecutil import list2vec
    >>> A = [list2vec([0, 2, 3]), list2vec([0, 4, 6]), list2vec([1, 2, 3])]
    >>> len(row_reduce(A))  # third row of A is 2x the first -> rank 2
    2
    """
    z = zero_vec(rowlist[0].D)
    return [row for row in echelon_form(rowlist) if row != z]


def null_space_basis(rowlist):
    """
    Return a basis for {u : u*A == 0}, the null space of A^T — Section 7.5.
    A row u_i of M pairs one-to-one with row i of echelon_form(rowlist); when
    that row of the echelon form is zero, u_i satisfies u_i * A == 0.

    >>> from coding_the_matrix.gf2 import one
    >>> from coding_the_matrix.vec import Vec
    >>> D = {'A', 'B', 'C', 'D', 'E'}
    >>> rows = {'a','b','c','d','e'}
    >>> A = [
    ...     Vec(D, {'D': one}),
    ...     Vec(D, {'D': one, 'E': one}),
    ...     Vec(D, {'A': one, 'D': one}),
    ...     Vec(D, {'A': one, 'B': one, 'C': one, 'E': one}),
    ...     Vec(D, {'A': one, 'D': one}),
    ... ]
    >>> basis = null_space_basis(A)
    >>> len(basis)
    1
    >>> u = basis[0]
    >>> u_dot_A = sum((u[i] * A[i] for i in range(5)), zero_vec(D))
    >>> [u_dot_A[c] for c in ('A', 'B', 'C', 'D', 'E')]
    [0, 0, 0, 0, 0]
    """
    M, U = _gaussian_elimination(rowlist)
    z = zero_vec(rowlist[0].D)
    return [m_row for m_row, u_row in zip(M, U) if u_row == z]
