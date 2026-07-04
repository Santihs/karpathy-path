import pytest

from coding_the_matrix.vec import Vec
from coding_the_matrix.vecutil import list2vec, zero_vec
from coding_the_matrix.triangular import triangular_solve, triangular_solve_n
from coding_the_matrix.gf2 import one


def test_zero_vec_is_all_implicit_zero():
    z = zero_vec({'a', 'b', 'c'})
    assert z['a'] == 0 and z['b'] == 0 and z['c'] == 0


def test_list2vec_indexes_from_zero():
    v = list2vec([7, 8, 9])
    assert v.D == {0, 1, 2}
    assert v[0] == 7 and v[2] == 9


def test_triangular_solve_n_book_example():
    rowlist = [
        Vec({0, 1, 2, 3}, {0: 1, 1: 0.5, 2: -2, 3: 4}),
        Vec({0, 1, 2, 3}, {1: 3, 2: 3, 3: 2}),
        Vec({0, 1, 2, 3}, {2: 1, 3: 5}),
        Vec({0, 1, 2, 3}, {3: 2}),
    ]
    b = [-8, 3, -4, 6]
    x = triangular_solve_n(rowlist, b)
    # solution must satisfy every equation, not just match hand-computed values
    assert [round(rowlist[i] * x, 6) for i in range(4)] == b


def test_triangular_solve_arbitrary_domain():
    label_list = ['a', 'b', 'c', 'd']
    D = set(label_list)
    rowlist = [
        Vec(D, {'a': 4, 'b': -2, 'c': 0.5, 'd': 1}),
        Vec(D, {'b': 2, 'c': 3, 'd': 3}),
        Vec(D, {'c': 5, 'd': 1}),
        Vec(D, {'d': 2.}),
    ]
    b = [6, -4, 3, -8]
    x = triangular_solve(rowlist, label_list, b)
    assert [round(rowlist[i] * x, 6) for i in range(4)] == b


def test_triangular_solve_n_zero_pivot_raises():
    # Prop. 2.11.6: a zero diagonal entry means the system has no solution
    # for some b. Caught explicitly with an assert (fails fast with a clear
    # message) rather than left to surface as a bare ZeroDivisionError.
    rowlist = [
        Vec({0, 1}, {0: 1, 1: 1}),
        Vec({0, 1}, {1: 0}),  # zero pivot at position 1
    ]
    with pytest.raises(AssertionError, match="zero pivot"):
        triangular_solve_n(rowlist, [3, 5])


def test_triangular_solve_n_over_gf2():
    # Sanity check the algorithm's field-genericity claim: it only needs
    # +, -, *, / on the diagonal entry, so it must work verbatim over GF(2),
    # where the only nonzero pivot value possible is `one`.
    rowlist = [
        Vec({0, 1}, {0: one, 1: one}),
        Vec({0, 1}, {1: one}),
    ]
    b = [one, 0]
    x = triangular_solve_n(rowlist, b)
    assert rowlist[0] * x == one
    assert rowlist[1] * x == 0
