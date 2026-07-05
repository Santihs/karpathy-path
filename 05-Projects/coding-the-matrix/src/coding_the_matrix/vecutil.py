# Klein, "Coding the Matrix", small Vec construction helpers.
from coding_the_matrix.vec import Vec


def list2vec(L):
    """
    Given a list L of field elements, return a Vec with domain {0...len(L)-1}
    whose entry i is L[i].

    >>> list2vec([10, 20, 30])
    Vec({0, 1, 2},{0: 10, 1: 20, 2: 30})
    """
    return Vec(set(range(len(L))), {k: L[k] for k in range(len(L))})


def zero_vec(D):
    """
    Returns the zero vector with the given domain.

    >>> zero_vec({'a', 'b'}) == Vec({'a', 'b'}, {})
    True
    """
    return Vec(D, {})


def lin_comb(vlist, clist):
    """
    Returns the linear combination of the vectors in vlist with the
    corresponding coefficients in clist.

    >>> lin_comb([list2vec([2, 3.5]), list2vec([4, 10])], [-5, 2]) == list2vec([-2, 2.5])
    True
    """
    return sum([coeff * v for (coeff, v) in zip(clist, vlist)])
