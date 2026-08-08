# Klein, "Coding the Matrix", Ch. 8 — The Inner Product.
#
# Splits b into a part parallel to v (b|v = sigma*v) and a part orthogonal to
# v (b_|v = b - b|v). The parallel part is the closest point to b on the line
# Span{v} — Fire Engine Lemma 8.3.8 — so project_along solves the fire-engine
# problem directly. sigma = <b,v>/<v,v> comes from requiring <b - sigma*v, v> = 0.
from coding_the_matrix.mat import Mat
from coding_the_matrix.vec import Vec

ZERO_THRESHOLD = 1e-20  # treat v as the zero vector if floating-point roundoff
# leaves it with a squared norm this small — see Section 8.3.4, "Beware!".


def project_along(b, v):
    """
    Returns the projection of b along v (i.e. b^||v = sigma*v), the point on
    Span{v} closest to b (Fire Engine Lemma 8.3.8).

    >>> from coding_the_matrix.vecutil import list2vec
    >>> project_along(list2vec([2, 4]), list2vec([6, 2])) == list2vec([3, 1])
    True
    >>> project_along(list2vec([1, 2]), list2vec([0, 0])) == list2vec([0, 0])
    True
    """
    sigma = (b * v) / (v * v) if v * v > ZERO_THRESHOLD else 0
    return sigma * v


def project_orthogonal_1(b, v):
    """
    Returns the projection of b orthogonal to v (i.e. b^perp_v = b - b^||v).

    >>> from coding_the_matrix.vecutil import list2vec
    >>> project_orthogonal_1(list2vec([2, 4]), list2vec([6, 2])) == list2vec([-1, 3])
    True
    """
    return b - project_along(b, v)


def projection_matrix(v):
    """
    Returns the matrix M such that M*x == project_along(x, v) for every x,
    via the outer product v*v^T / <v,v> (Section 8.3.6). Correct even if
    ||v|| != 1, and correct (the zero matrix) if v is the zero vector.

    >>> from coding_the_matrix.vecutil import list2vec
    >>> M = projection_matrix(list2vec([6, 2]))
    >>> Mx = M * list2vec([2, 4])
    >>> abs(Mx[0] - 3) < 1e-9 and abs(Mx[1] - 1) < 1e-9
    True
    """
    denom = v * v
    scale = 1 / denom if denom > ZERO_THRESHOLD else 0
    return Mat((v.D, v.D), {(r, c): scale * v[r] * v[c] for r in v.D for c in v.D})
