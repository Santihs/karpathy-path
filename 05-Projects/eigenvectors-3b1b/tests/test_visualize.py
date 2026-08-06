import numpy as np

from eigenvectors_3b1b.visualize import eigen_real_directions


def test_finds_two_real_eigenvectors_for_shear_matrix():
    A = np.array([[3.0, 1.0], [0.0, 2.0]])
    pairs = eigen_real_directions(A)
    values = sorted(val for _, val in pairs)
    assert np.allclose(values, [2.0, 3.0])


def test_no_real_eigenvectors_for_pure_rotation():
    # 90-degree rotation matrix — eigenvalues are +-i, no real eigenvector.
    A = np.array([[0.0, -1.0], [1.0, 0.0]])
    assert eigen_real_directions(A) == []


def test_eigenvector_stays_on_its_own_span():
    A = np.array([[3.0, 1.0], [0.0, 2.0]])
    for vec, val in eigen_real_directions(A):
        assert np.allclose(A @ vec, val * vec)
