import numpy as np
import pytest

from eigenvectors_3b1b.fib_eigen import A_FIB, fib, matrix_power_via_eigenbasis


def direct_fib(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


@pytest.mark.parametrize("n", range(15))
def test_fib_matches_direct_computation(n):
    assert fib(n) == direct_fib(n)


@pytest.mark.parametrize("n", [1, 2, 5, 10])
def test_matrix_power_matches_numpy_matrix_power(n):
    got = matrix_power_via_eigenbasis(A_FIB, n)
    expected = np.linalg.matrix_power(A_FIB, n)
    assert np.allclose(got, expected)


def test_eigenvectors_match_derived_by_hand():
    # v1 = [2, 1+sqrt(5)], v2 = [2, 1-sqrt(5)] from the 3B1B exercise —
    # verify they actually satisfy A@v = lambda*v for A's real eigenvalues.
    sqrt5 = np.sqrt(5)
    phi = (1 + sqrt5) / 2
    psi = (1 - sqrt5) / 2
    v1 = np.array([2.0, 1 + sqrt5])
    v2 = np.array([2.0, 1 - sqrt5])

    assert np.allclose(A_FIB @ v1, phi * v1)
    assert np.allclose(A_FIB @ v2, psi * v2)
