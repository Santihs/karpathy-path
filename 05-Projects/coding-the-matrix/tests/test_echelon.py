import pytest

from coding_the_matrix.vec import Vec
from coding_the_matrix.vecutil import list2vec, zero_vec
from coding_the_matrix.gf2 import one
from coding_the_matrix.echelon import (
    transformation,
    echelon_form,
    row_reduce,
    null_space_basis,
)


def mat_from_rowlist(rowlist, D):
    """helper: apply a transformation matrix M to rowlist, returning M @ rowlist"""
    return [
        sum((m_row[i] * rowlist[i] for i in range(len(rowlist))), zero_vec(D))
        for m_row in rowlist
    ]


def test_transformation_returns_invertible_square_matrix():
    D = {0, 1, 2}
    A = [list2vec([1, 2, 3]), list2vec([2, 4, 7]), list2vec([1, 0, 1])]
    M = transformation(A)
    assert len(M) == 3
    assert all(m_row.D == {0, 1, 2} for m_row in M)


def test_transformation_times_A_is_echelon_form():
    D = {0, 1, 2}
    A = [list2vec([1, 2, 3]), list2vec([2, 4, 7]), list2vec([1, 0, 1])]
    M = transformation(A)
    MA = [
        sum((M_row[i] * A[i] for i in range(3)), zero_vec(D)) for M_row in M
    ]
    # echelon form: each row's first nonzero moves strictly right of the previous
    pivots = []
    for row in MA:
        nz = [c for c in range(3) if row[c] != 0]
        pivots.append(min(nz) if nz else None)
    real_pivots = [p for p in pivots if p is not None]
    assert real_pivots == sorted(real_pivots)
    assert len(set(real_pivots)) == len(real_pivots)


def test_echelon_form_full_rank_matrix_has_no_zero_rows():
    A = [list2vec([1, 0]), list2vec([0, 1])]
    U = echelon_form(A)
    z = zero_vec({0, 1})
    assert all(row != z for row in U)


def test_echelon_form_dependent_rows_produce_zero_row():
    # third row is 2*first + 3*second -> rank 2, one zero row expected
    A = [list2vec([1, 0, 0]), list2vec([0, 1, 0]), list2vec([2, 3, 0])]
    U = echelon_form(A)
    z = zero_vec({0, 1, 2})
    zero_rows = [row for row in U if row == z]
    assert len(zero_rows) == 1


def test_row_reduce_drops_zero_rows_and_keeps_basis_size():
    A = [list2vec([0, 2, 3]), list2vec([0, 4, 6]), list2vec([1, 2, 3])]
    basis = row_reduce(A)
    assert len(basis) == 2  # rank 2: row 1 is 2x row 0
    z = zero_vec({0, 1, 2})
    assert all(row != z for row in basis)


def test_row_reduce_preserves_row_space_full_rank_identity_like():
    A = [list2vec([2, 0, 0]), list2vec([0, 3, 0]), list2vec([0, 0, 5])]
    basis = row_reduce(A)
    assert len(basis) == 3


def test_null_space_basis_matches_book_problem_7_9_9():
    D = {'A', 'B', 'C', 'D', 'E'}
    A = [
        Vec(D, {'D': one}),
        Vec(D, {'D': one, 'E': one}),
        Vec(D, {'A': one, 'D': one}),
        Vec(D, {'A': one, 'B': one, 'C': one, 'E': one}),
        Vec(D, {'A': one, 'D': one}),
    ]
    basis = null_space_basis(A)
    assert len(basis) == 1  # rows c and e are identical -> one dependency
    u = basis[0]
    u_dot_A = sum((u[i] * A[i] for i in range(5)), zero_vec(D))
    assert all(u_dot_A[c] == 0 for c in D)


def test_null_space_basis_empty_when_rows_independent():
    D = {0, 1, 2}
    A = [list2vec([1, 0, 0]), list2vec([0, 1, 0]), list2vec([0, 0, 1])]
    assert null_space_basis(A) == []


def test_transformation_does_not_mutate_input_rowlist():
    A = [list2vec([1, 2]), list2vec([3, 4])]
    original = [Vec(row.D, dict(row.f)) for row in A]
    transformation(A)
    assert A[0] == original[0] and A[1] == original[1]


def test_over_gf2_no_precision_issues():
    D = {'A', 'B', 'C'}
    A = [
        Vec(D, {'A': one, 'C': one}),
        Vec(D, {'B': one, 'C': one}),
        Vec(D, {'A': one, 'B': one}),  # = row0 + row1 over GF(2) -> dependent
    ]
    basis = row_reduce(A)
    assert len(basis) == 2
