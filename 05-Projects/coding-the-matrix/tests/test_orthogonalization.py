import math

import pytest

from coding_the_matrix.matutil import listlist2mat
from coding_the_matrix.mat import Mat
from coding_the_matrix.vecutil import list2vec
from coding_the_matrix.orthogonalization import (
    project_along,
    project_orthogonal_1,
    projection_matrix,
    project_orthogonal,
    aug_project_orthogonal,
    orthogonalize,
    aug_orthogonalize,
    closest_point,
    find_basis,
    find_subset_basis,
    find_orthogonal_complement,
    qr_factor,
    QR_solve,
    approx_mat_equal,
)


def approx_equal(u, v, tol=1e-9):
    # projection_matrix goes through a division (1/<v,v>) baked into every
    # entry, so results land a float epsilon off exact values -- Vec.__eq__
    # is exact equality, so floating comparisons here need their own check.
    assert u.D == v.D
    return all(abs(u[k] - v[k]) < tol for k in u.D)


def test_project_along_fire_engine_example():
    # Klein Example 8.3.14: v=[6,2], b=[2,4] -> closest point [3,1]
    v = list2vec([6, 2])
    b = list2vec([2, 4])
    assert project_along(b, v) == list2vec([3, 1])


def test_fire_engine_distance_saves_the_house():
    v = list2vec([6, 2])
    b = list2vec([2, 4])
    closest = project_along(b, v)
    distance = math.sqrt((b - closest) * (b - closest))
    assert distance == pytest.approx(math.sqrt(10))
    assert distance < 3.5  # length of the firehose


def test_project_orthogonal_fire_engine_example():
    v = list2vec([6, 2])
    b = list2vec([2, 4])
    assert project_orthogonal_1(b, v) == list2vec([-1, 3])


def test_parallel_plus_orthogonal_reconstructs_b():
    v = list2vec([6, 2])
    b = list2vec([2, 4])
    assert project_along(b, v) + project_orthogonal_1(b, v) == b


def test_orthogonal_part_is_orthogonal_to_v():
    v = list2vec([6, 2])
    b = list2vec([2, 4])
    assert project_orthogonal_1(b, v) * v == 0


def test_project_along_zero_vector_returns_zero():
    # Example 8.3.10: v is the zero vector -> b|v = 0, b_|v = b
    v = list2vec([0, 0])
    b = list2vec([5, -3])
    assert project_along(b, v) == list2vec([0, 0])
    assert project_orthogonal_1(b, v) == b


def test_project_along_axis_example():
    # Example 8.3.7: v=(1,0) -> b|v=(b1,0), b_|v=(0,b2)
    v = list2vec([1, 0])
    b = list2vec([3, 7])
    assert project_along(b, v) == list2vec([3, 0])
    assert project_orthogonal_1(b, v) == list2vec([0, 7])


def test_project_along_b_already_on_line():
    v = list2vec([2, 0])
    b = list2vec([5, 0])
    assert project_along(b, v) == b
    assert project_orthogonal_1(b, v) == list2vec([0, 0])


def test_project_along_b_already_orthogonal_to_v():
    v = list2vec([1, 0])
    b = list2vec([0, 4])
    assert project_along(b, v) == list2vec([0, 0])
    assert project_orthogonal_1(b, v) == b


def test_projection_matrix_matches_project_along():
    v = list2vec([6, 2])
    b = list2vec([2, 4])
    M = projection_matrix(v)
    assert approx_equal(M * b, project_along(b, v))


def test_projection_matrix_symmetric():
    v = list2vec([3, -1, 2])
    M = projection_matrix(v)
    assert M == M.transpose()


def test_projection_matrix_image_is_span_v():
    # Problem 8.3.16: M = v v^T / <v,v> has rank 1 -- M*x always lands on Span{v}.
    v = list2vec([3, -1, 2])
    M = projection_matrix(v)
    for x in [list2vec([1, 0, 0]), list2vec([0, 1, 0]), list2vec([5, -2, 7])]:
        Mx = M * x
        sigma = Mx[0] / v[0]  # v[0]=3 != 0 here, safe to use as the scaling check
        assert approx_equal(Mx, sigma * v)


def test_projection_matrix_kernel_is_orthogonal_complement():
    v = list2vec([3, -1, 2])
    M = projection_matrix(v)
    w = list2vec([1, 3, 0])  # w * v == 0, i.e. w is orthogonal to v
    assert w * v == 0
    assert M * w == list2vec([0, 0, 0])


def test_projection_matrix_idempotent():
    # A projection applied twice does nothing new: M*M*x == M*x
    v = list2vec([3, -1, 2])
    b = list2vec([1, 5, -2])
    M = projection_matrix(v)
    assert approx_equal(M * (M * b), M * b)


def test_projection_matrix_zero_vector_is_zero_matrix():
    v = list2vec([0, 0])
    M = projection_matrix(v)
    b = list2vec([9, -4])
    assert M * b == list2vec([0, 0])


# --- Ch. 9: project_orthogonal, requires mutually orthogonal vlist ---


def test_project_orthogonal_on_mutually_orthogonal_vlist():
    vlist = [list2vec([1, 0, 0]), list2vec([0, 1, 0])]
    b = list2vec([1, 2, 3])
    b_perp = project_orthogonal(b, vlist)
    assert b_perp == list2vec([0, 0, 3])
    assert all(b_perp * v == 0 for v in vlist)


def test_project_orthogonal_empty_vlist_returns_b():
    b = list2vec([1, 2, 3])
    assert project_orthogonal(b, []) == b


def test_project_orthogonal_fails_on_non_orthogonal_vlist():
    # Sec 9.1.3: the book's own counterexample -- sequential subtraction
    # against a NON-orthogonal vlist reintroduces a component along v1 that
    # step 1 already zeroed out. This documents the failure, it doesn't
    # mean the function is buggy -- the spec only promises correctness for
    # mutually orthogonal vlist (Theorem 9.2.3).
    root2over2 = 2**0.5 / 2
    vlist = [list2vec([1, 0]), list2vec([root2over2, root2over2])]
    b = list2vec([1, 1])
    b_perp = project_orthogonal(b, vlist)
    assert b_perp * vlist[0] != 0  # no longer orthogonal to v1 -- the bug in action


# --- aug_project_orthogonal: coefficients + reconstruction (Eq 9.3/9.5) ---


def test_aug_project_orthogonal_reconstructs_b():
    vlist = [list2vec([1, 0, 0]), list2vec([0, 1, 0])]
    b = list2vec([1, 2, 3])
    b_perp, sigmadict = aug_project_orthogonal(b, vlist)
    reconstructed = sigmadict[0] * vlist[0] + sigmadict[1] * vlist[1] + sigmadict[2] * b_perp
    assert reconstructed == b


def test_aug_project_orthogonal_b_perp_coefficient_is_always_one():
    vlist = [list2vec([3, -1, 2])]
    _, sigmadict = aug_project_orthogonal(list2vec([1, 5, -2]), vlist)
    assert sigmadict[len(vlist)] == 1


# --- orthogonalize (Gram-Schmidt), Sec 9.3 ---


def test_orthogonalize_klein_example_9_3_2():
    vlist = [list2vec([2, 0, 0]), list2vec([1, 2, 2]), list2vec([1, 0, 2])]
    vstarlist = orthogonalize(vlist)
    assert vstarlist == [list2vec([2, 0, 0]), list2vec([0, 2, 2]), list2vec([0, -1, 1])]


def test_orthogonalize_result_is_mutually_orthogonal():
    vlist = [list2vec([2, 0, 0]), list2vec([1, 2, 2]), list2vec([1, 0, 2])]
    vstarlist = orthogonalize(vlist)
    for i in range(len(vstarlist)):
        for j in range(i + 1, len(vstarlist)):
            assert vstarlist[i] * vstarlist[j] == 0


def test_orthogonalize_preserves_span():
    # Lemma 9.3.5: each vi is a linear combination of the v*'s and vice versa.
    # Cheap check: closest_point of each original vi against vstarlist is vi itself.
    vlist = [list2vec([2, 0, 0]), list2vec([1, 2, 2]), list2vec([1, 0, 2])]
    vstarlist = orthogonalize(vlist)
    for v in vlist:
        assert closest_point(v, vstarlist) == v


def test_orthogonalize_linearly_dependent_input_gives_zero_vector():
    vlist = [list2vec([2, 0]), list2vec([4, 0])]  # v2 is a multiple of v1
    vstarlist = orthogonalize(vlist)
    assert vstarlist[1] == list2vec([0, 0])


def test_orthogonalize_order_matters():
    # Remark 9.3.6: reversing vlist does not mirror the result.
    vlist = [list2vec([2, 0, 0]), list2vec([1, 2, 2]), list2vec([1, 0, 2])]
    forward = orthogonalize(vlist)
    backward = orthogonalize(list(reversed(vlist)))
    assert forward != list(reversed(backward))


# --- aug_orthogonalize: R matrix as per-vector coefficient Vecs (9.5.3) ---


def test_aug_orthogonalize_reconstructs_each_original_vector():
    vlist = [list2vec([2, 0, 0]), list2vec([1, 2, 2]), list2vec([1, 0, 2])]
    vstarlist, sigma_vecs = aug_orthogonalize(vlist)
    for i, v in enumerate(vlist):
        reconstructed = sum(sigma_vecs[i][j] * vstarlist[j] for j in range(len(vstarlist)))
        assert approx_equal(reconstructed, v)


def test_aug_orthogonalize_matches_orthogonalize():
    vlist = [list2vec([2, 0, 0]), list2vec([1, 2, 2]), list2vec([1, 0, 2])]
    vstarlist, _ = aug_orthogonalize(vlist)
    assert vstarlist == orthogonalize(vlist)


# --- closest_point (Sec 9.4) ---


def test_closest_point_klein_example_9_4_1():
    vlist = [list2vec([8, -2, 2]), list2vec([4, 2, 4])]
    b = list2vec([5, -5, 2])
    assert closest_point(b, vlist) == list2vec([6, -3, 0])


def test_closest_point_is_in_the_span():
    # closest_point(b, vlist) should be expressible using only vlist's basis --
    # cheap check: it's its own closest point (already lives in the span).
    vlist = [list2vec([2, 0, 0]), list2vec([1, 2, 2])]
    b = list2vec([5, -5, 2])
    p = closest_point(b, vlist)
    assert closest_point(p, vlist) == p


def test_closest_point_b_already_in_span_returns_b():
    vlist = [list2vec([1, 0, 0]), list2vec([0, 1, 0])]
    b = list2vec([3, 7, 0])
    assert closest_point(b, vlist) == b


def test_closest_point_distance_is_minimal():
    vlist = [list2vec([1, 0, 0]), list2vec([0, 1, 0])]
    b = list2vec([3, 7, 5])
    p = closest_point(b, vlist)
    dist_p = math.sqrt((b - p) * (b - p))
    other = list2vec([2, 6, 0])  # a different point in Span(vlist)
    dist_other = math.sqrt((b - other) * (b - other))
    assert dist_p < dist_other


# --- find_basis / find_subset_basis (Sec 9.5.1-9.5.2) ---


def test_find_basis_drops_dependent_vector():
    vlist = [list2vec([2, 0, 0]), list2vec([1, 2, 2]), list2vec([3, 2, 2])]  # v3 = v1 + v2
    basis = find_basis(vlist)
    assert len(basis) == 2


def test_find_basis_is_mutually_orthogonal_and_nonzero():
    vlist = [list2vec([2, 0, 0]), list2vec([1, 2, 2]), list2vec([3, 2, 2])]
    basis = find_basis(vlist)
    for v in basis:
        assert v * v > 0
    for i in range(len(basis)):
        for j in range(i + 1, len(basis)):
            assert basis[i] * basis[j] == 0


def test_find_subset_basis_uses_original_vectors():
    vlist = [list2vec([2, 0, 0]), list2vec([1, 2, 2]), list2vec([3, 2, 2])]  # v3 = v1 + v2
    basis = find_subset_basis(vlist)
    assert basis == [vlist[0], vlist[1]]
    for v in basis:
        assert v in vlist


def test_find_subset_basis_spans_same_space_as_find_basis():
    vlist = [list2vec([2, 0, 0]), list2vec([1, 2, 2]), list2vec([3, 2, 2])]
    subset_basis = find_subset_basis(vlist)
    starred_basis = find_basis(vlist)
    assert len(subset_basis) == len(starred_basis)
    for v in subset_basis:
        assert closest_point(v, starred_basis) == v


def test_find_basis_all_independent_keeps_everything():
    vlist = [list2vec([1, 0, 0]), list2vec([0, 1, 0]), list2vec([0, 0, 1])]
    assert len(find_basis(vlist)) == 3
    assert len(find_subset_basis(vlist)) == 3


# --- find_orthogonal_complement (Sec 9.6.6) ---


def test_find_orthogonal_complement_klein_example_9_6_7():
    U_basis = [list2vec([8, -2, 2]), list2vec([0, 3, 3])]
    W_basis = [list2vec([1, 0, 0]), list2vec([0, 1, 0]), list2vec([0, 0, 1])]
    basis = find_orthogonal_complement(U_basis, W_basis)
    assert len(basis) == 1
    assert approx_equal(basis[0], list2vec([1 / 9, 2 / 9, -2 / 9]))


def test_find_orthogonal_complement_is_orthogonal_to_U():
    U_basis = [list2vec([8, -2, 2]), list2vec([0, 3, 3])]
    W_basis = [list2vec([1, 0, 0]), list2vec([0, 1, 0]), list2vec([0, 0, 1])]
    basis = find_orthogonal_complement(U_basis, W_basis)
    for v in basis:
        for u in U_basis:
            assert abs(v * u) < 1e-9


def test_find_orthogonal_complement_dimension_matches_direct_sum():
    # dim(complement) == dim(W) - dim(U) -- Direct-Sum Dimension Corollary 6.3.9
    U_basis = [list2vec([1, 1, 0, 0]), list2vec([0, 0, 1, 1])]
    W_basis = [
        list2vec([1, 0, 0, 0]), list2vec([0, 1, 0, 0]),
        list2vec([0, 0, 1, 0]), list2vec([0, 0, 0, 1]),
    ]
    basis = find_orthogonal_complement(U_basis, W_basis)
    assert len(basis) == len(W_basis) - len(U_basis)


# --- qr_factor / QR_solve (Sec 9.7-9.8) ---


def test_qr_factor_reconstructs_A():
    A = listlist2mat([[3, 1], [1, 2], [2, -1]])
    Q, R = qr_factor(A)
    assert approx_mat_equal(Q * R, A)


def test_qr_factor_Q_is_column_orthogonal():
    A = listlist2mat([[3, 1], [1, 2], [2, -1]])
    Q, R = qr_factor(A)
    identity = Mat((Q.D[1], Q.D[1]), {(c, c): 1 for c in Q.D[1]})
    assert approx_mat_equal(Q.transpose() * Q, identity)


def test_qr_factor_R_is_upper_triangular_nonzero_diagonal():
    A = listlist2mat([[3, 1], [1, 2], [2, -1]])
    _, R = qr_factor(A)
    cols = sorted(R.D[1], key=str)
    for i, ci in enumerate(cols):
        for j, cj in enumerate(cols):
            if i > j:
                assert R[ci, cj] == 0
        assert abs(R[ci, ci]) > 1e-9


def test_qr_factor_dependent_columns_raises():
    A = listlist2mat([[1, 2], [2, 4], [3, 6]])  # col 1 = 2 * col 0
    with pytest.raises(ValueError):
        qr_factor(A)


def test_QR_solve_square_case():
    A = listlist2mat([[3, 1], [1, 2]])
    x = QR_solve(A, list2vec([9, 8]))
    assert A * x == list2vec([9, 8])


def test_QR_solve_least_squares_matches_closest_point():
    # Klein Example 9.4.1: A's columns are v1=[8,-2,2], v2=[4,2,4]
    A = listlist2mat([[8, 4], [-2, 2], [2, 4]])
    b = list2vec([5, -5, 2])
    x = QR_solve(A, b)
    vlist = [list2vec([8, -2, 2]), list2vec([4, 2, 4])]
    assert approx_equal(A * x, closest_point(b, vlist))


def test_QR_solve_least_squares_minimizes_residual():
    # x from QR_solve should give a strictly smaller residual than a
    # different, arbitrary x -- confirms it's actually the best fit.
    A = listlist2mat([[1, 0], [0, 1], [1, 1]])
    b = list2vec([1, 1, 3])
    x = QR_solve(A, b)
    residual = A * x - b
    dist = math.sqrt(residual * residual)
    other_x = list2vec([1, 1])
    other_residual = A * other_x - b
    other_dist = math.sqrt(other_residual * other_residual)
    assert dist <= other_dist + 1e-9
