import numpy as np

A_FIB = np.array([[0.0, 1.0], [1.0, 1.0]])


def matrix_power_via_eigenbasis(A: np.ndarray, n: int) -> np.ndarray:
    """A^n = M @ D^n @ M^-1, where M's columns are eigenvectors of A
    and D is diagonal with A's eigenvalues. Diagonal matrices raise to
    a power entry-by-entry, so this is cheap even for huge n."""
    eigenvalues, M = np.linalg.eig(A)
    D_n = np.diag(eigenvalues**n)
    return (M @ D_n @ np.linalg.inv(M)).real


def fib(n: int) -> int:
    """nth Fibonacci number (fib(0)=0, fib(1)=1) read off A^n's [0,1] entry."""
    An = matrix_power_via_eigenbasis(A_FIB, n)
    return round(An[0, 1])
