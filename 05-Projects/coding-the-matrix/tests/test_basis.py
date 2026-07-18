from coding_the_matrix.basis import grow, shrink, is_in_span
from coding_the_matrix.vecutil import list2vec


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
