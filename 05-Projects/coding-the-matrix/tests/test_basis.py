from coding_the_matrix.basis import grow, shrink, is_in_span, rank, is_independent, is_invertible
from coding_the_matrix.vec import Vec
from coding_the_matrix.vecutil import list2vec
from coding_the_matrix.matutil import listlist2mat
from coding_the_matrix.mat import Mat
from coding_the_matrix import gf2


def test_is_in_span_dependent_vector():
    a1, a2 = list2vec([1, 0]), list2vec([0, 1])
    a3 = a1 + a2
    assert is_in_span([a1, a2], a3)


def test_is_in_span_new_direction():
    a1, a2 = list2vec([1, 0]), list2vec([0, 1])
    assert not is_in_span([a1], a2)


def test_is_in_span_empty_set_only_contains_zero():
    zero = list2vec([0, 0, 0])
    nonzero = list2vec([1, 0, 0])
    assert is_in_span([], zero)
    assert not is_in_span([], nonzero)


def test_grow_standard_basis_r3_keeps_all_three():
    e1, e2, e3 = list2vec([1, 0, 0]), list2vec([0, 1, 0]), list2vec([0, 0, 1])
    basis = grow([e1, e2, e3])
    assert len(basis) == 3
    assert is_in_span(basis, list2vec([5, -2, 7]))


def test_grow_drops_redundant_vector():
    a1, a2 = list2vec([1, 0]), list2vec([0, 1])
    a3 = a1 + a2  # dependent — direction "looks new" but is reachable via a1,a2
    basis = grow([a1, a2, a3])
    assert len(basis) == 2
    assert not any(v is a3 for v in basis)  # a3 wasn't a new direction, so never added


def test_shrink_example_5_3_2_finds_minimum():
    v1, v2 = list2vec([1, 0, 0]), list2vec([0, 1, 0])
    v3 = v1 + 2 * v2   # = [1, 2, 0], redundant
    v4 = 3 * v1 + v2   # = [3, 1, 0], redundant
    original = [v1, v2, v3, v4]
    basis = shrink(original)
    assert len(basis) == 2
    # minimal set must still span exactly what the original set spanned
    assert all(is_in_span(basis, v) for v in original)


def test_shrink_cannot_go_below_dimension():
    v1, v2 = list2vec([1, 0]), list2vec([0, 1])
    basis = shrink([v1, v2])
    assert len(basis) == 2  # neither is redundant — both directions are needed


def test_rank_counts_independent_directions_only():
    a1, a2 = list2vec([1, 0, 0]), list2vec([0, 1, 0])
    a3 = a1 + a2  # redundant, Klein 6.2.6 style
    assert rank([a1, a2, a3]) == 2


def test_rank_at_most_cardinality():
    # Klein Proposition 6.2.17: rank(S) <= |S|, always.
    vectors = [list2vec([1, 0]), list2vec([0, 1]), list2vec([1, 1]), list2vec([2, 2])]
    assert rank(vectors) <= len(vectors)


def test_is_independent_dependent_set_over_reals():
    # Klein 6.7.6, first example set: dependent (8*[2,4,0]-4*[0,0,7]... == 4*[8,16,4] pattern)
    vectors = [list2vec(v) for v in [[2, 4, 0], [8, 16, 4], [0, 0, 7]]]
    assert not is_independent(vectors)


def test_is_independent_independent_set_over_reals():
    vectors = [list2vec(v) for v in [[1, 3, 0, 0], [2, 0, 5, 1], [0, 0, 1, 0], [0, 0, 7, -1]]]
    assert is_independent(vectors)


def test_is_independent_over_gf2():
    D = {0, 1, 2, 3}
    one = gf2.one
    v1 = Vec(D, {0: one, 2: one})
    v2 = Vec(D, {1: one})
    v3 = Vec(D, {0: one, 1: one, 2: one, 3: one})
    v4 = Vec(D, {3: one})
    assert not is_independent([v1, v2, v3, v4])


def test_is_invertible_nonsquare_is_never_invertible():
    assert not is_invertible(listlist2mat([[1, 2, 3], [3, 1, 1]]))
    assert not is_invertible(listlist2mat([[1, 0], [0, 1], [2, 1]]))


def test_is_invertible_square_upper_triangular_nonzero_diagonal():
    M = listlist2mat([[1, 0, 1, 0], [0, 2, 1, 0], [0, 0, 3, 1], [0, 0, 0, 4]])
    assert is_invertible(M)


def test_is_invertible_square_dependent_columns():
    assert not is_invertible(listlist2mat([[1, 2], [2, 4]]))  # col2 = 2*col1


def test_is_invertible_identity_is_invertible():
    assert is_invertible(listlist2mat([[1, 0], [0, 1]]))


def test_is_invertible_gf2_same_pattern_as_real_but_different_result():
    # Klein 6.7.12: same 0/1 pattern over R is invertible, over GF(2) it is not
    # (2 = 0 in GF(2), so the row-reduction that works over R collapses here).
    real_M = listlist2mat([[1, 0, 1], [0, 1, 1], [1, 1, 0]])
    assert is_invertible(real_M)

    one = gf2.one
    D = {0, 1, 2}
    gf2_M = Mat((D, D), {(0, 0): one, (0, 2): one, (1, 1): one, (1, 2): one, (2, 0): one, (2, 1): one})
    assert not is_invertible(gf2_M)
