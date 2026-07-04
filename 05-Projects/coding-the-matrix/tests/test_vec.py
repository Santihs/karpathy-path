import math

import pytest

from coding_the_matrix.vec import Vec


def test_getitem_missing_key_is_zero():
    v = Vec({'a', 'b', 'c'}, {'a': 2})
    assert v['b'] == 0


def test_getitem_present_key():
    v = Vec({'a', 'b'}, {'a': 2, 'b': 5})
    assert v['b'] == 5


def test_setitem_overwrites_and_creates():
    v = Vec({'a', 'b'}, {'a': 1})
    v['a'] = 9
    v['b'] = 3
    assert v['a'] == 9
    assert v['b'] == 3


def test_equal_ignores_explicit_vs_implicit_zero():
    assert Vec({'a', 'b'}, {'a': 0}) == Vec({'a', 'b'}, {})


def test_equal_requires_same_domain():
    with pytest.raises(AssertionError):
        Vec({'a'}, {}) == Vec({'a', 'b'}, {})


def test_add_over_disjoint_sparse_keys():
    a = Vec({'x', 'y', 'z'}, {'x': 1})
    b = Vec({'x', 'y', 'z'}, {'y': 2})
    assert a + b == Vec({'x', 'y', 'z'}, {'x': 1, 'y': 2})


def test_add_is_commutative():
    a = Vec({'x', 'y'}, {'x': 3, 'y': -1})
    b = Vec({'x', 'y'}, {'x': -3, 'y': 4})
    assert a + b == b + a


def test_dot_orthogonal_basis_vectors_is_zero():
    e1 = Vec({'x', 'y'}, {'x': 1})
    e2 = Vec({'x', 'y'}, {'y': 1})
    assert e1 * e2 == 0


def test_dot_matches_naive_dense_computation():
    domain = ['a', 'b', 'c', 'd']
    u_vals = [3, -2, 0, 7]
    v_vals = [1, 5, 9, -1]
    u = Vec(set(domain), dict(zip(domain, u_vals)))
    v = Vec(set(domain), dict(zip(domain, v_vals)))
    expected = sum(x * y for x, y in zip(u_vals, v_vals))
    assert u * v == expected


# --- weakness case -----------------------------------------------------
#
# equal() does exact per-key comparison (getitem(u,k) == getitem(v,k)).
# That's correct for exact fields (int, GF(2)) but breaks for float fields,
# where accumulated rounding error means mathematically-equal vectors compare
# unequal. Klein's own reference solution works around this with a separate
# is_almost_zero() helper on (u - v) instead of baking tolerance into __eq__ —
# because __eq__ must stay exact for exact fields; a single equal() can't be
# both exact and tolerant at once. This test documents the failure so we
# don't "fix" equal() into something that breaks GF(2)/int correctness.
def test_equal_is_exact_and_breaks_on_float_accumulation():
    u = Vec({'x'}, {'x': 0.1}) + Vec({'x'}, {'x': 0.2})
    v = Vec({'x'}, {'x': 0.3})
    assert u['x'] != v['x']  # 0.30000000000000004 != 0.3
    assert not (u == v)      # exact equal() correctly reports them as different

    # improvement: compare with tolerance at the call site, not inside equal()
    assert math.isclose(u['x'], v['x'], abs_tol=1e-9)
