import math

import pytest

from coding_the_matrix.vecutil import list2vec
from coding_the_matrix.orthogonalization import (
    project_along,
    project_orthogonal_1,
    projection_matrix,
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
