# Klein, "Coding the Matrix", Ch. 8 — The Inner Product.
#
# Splits b into a part parallel to v (b|v = sigma*v) and a part orthogonal to
# v (b_|v = b - b|v). The parallel part is the closest point to b on the line
# Span{v} — Fire Engine Lemma 8.3.8 — so project_along solves the fire-engine
# problem directly. sigma = <b,v>/<v,v> comes from requiring <b - sigma*v, v> = 0.
from coding_the_matrix.mat import Mat
from coding_the_matrix.vec import Vec
from coding_the_matrix.triangular import triangular_solve

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


# Klein, Ch. 9 — Orthogonalization.
#
# project_orthogonal only guarantees a correct b_|V for vlist that is
# MUTUALLY orthogonal (Sec 9.1.3: sequential subtraction against a
# non-orthogonal vlist reintroduces components an earlier step already
# zeroed out). orthogonalize (Gram-Schmidt) is what produces a mutually
# orthogonal vlist with the same span in the first place -- the two
# functions are meant to be used together (Sec 9.4).


def project_orthogonal(b, vlist):
    """
    Returns the projection of b orthogonal to Span(vlist) -- b^perp_V.
    Only correct if vlist is mutually orthogonal (Theorem 9.2.3); each
    step subtracts b's component along one vi, which by construction
    doesn't reintroduce a component along any earlier vj (Lemma 9.2.4).

    >>> from coding_the_matrix.vecutil import list2vec
    >>> vlist = [list2vec([1, 0, 0]), list2vec([0, 1, 0])]
    >>> project_orthogonal(list2vec([1, 2, 3]), vlist) == list2vec([0, 0, 3])
    True
    """
    for v in vlist:
        b = project_orthogonal_1(b, v)
    return b


def aug_project_orthogonal(b, vlist):
    """
    Like project_orthogonal, but also returns the coefficients used at each
    step (Sec 9.2.2, Eq 9.3/9.5): b == sum(sigma_i * vlist[i] for i) + b_perp,
    with the coefficient for b_perp itself always 1. sigmadict is keyed by
    the index into vlist, plus len(vlist) for the b_perp coefficient.

    >>> from coding_the_matrix.vecutil import list2vec
    >>> vlist = [list2vec([1, 0, 0]), list2vec([0, 1, 0])]
    >>> b_perp, sigmadict = aug_project_orthogonal(list2vec([1, 2, 3]), vlist)
    >>> b_perp == list2vec([0, 0, 3])
    True
    >>> sigmadict == {0: 1, 1: 2, 2: 1}
    True
    """
    sigmadict = {len(vlist): 1}
    for i, v in enumerate(vlist):
        sigma = (b * v) / (v * v) if v * v > ZERO_THRESHOLD else 0
        sigmadict[i] = sigma
        b = b - sigma * v
    return b, sigmadict


def orthogonalize(vlist):
    """
    Gram-Schmidt: turns any vlist into a mutually orthogonal vstarlist with
    the same span (Sec 9.3.1). Each vi is projected orthogonal to whatever
    is already in vstarlist -- which, by the previous iteration, is already
    mutually orthogonal, so project_orthogonal stays valid at every step
    (Lemma 9.3.1). If vlist is linearly dependent, some vi* comes out the
    zero vector.

    >>> from coding_the_matrix.vecutil import list2vec
    >>> vlist = [list2vec([2, 0, 0]), list2vec([1, 2, 2]), list2vec([1, 0, 2])]
    >>> orthogonalize(vlist) == [list2vec([2, 0, 0]), list2vec([0, 2, 2]), list2vec([0, -1, 1])]
    True
    """
    vstarlist = []
    for v in vlist:
        vstarlist.append(project_orthogonal(v, vstarlist))
    return vstarlist


def aug_orthogonalize(vlist):
    """
    Like orthogonalize, but also returns the coefficients needed to
    reconstruct each original vi from vstarlist (Sec 9.5.3) -- the R matrix
    of Eq 9.7, made explicit as one coefficient-Vec per original vi:
    [v1|...|vn] == [v1*|...|vn*] * [u1|...|un].

    >>> from coding_the_matrix.vecutil import list2vec
    >>> vlist = [list2vec([2, 0, 0]), list2vec([1, 2, 2])]
    >>> vstarlist, sigma_vecs = aug_orthogonalize(vlist)
    >>> vstarlist == [list2vec([2, 0, 0]), list2vec([0, 2, 2])]
    True
    >>> sigma_vecs[1][0] * vstarlist[0] + sigma_vecs[1][1] * vstarlist[1] == vlist[1]
    True
    """
    vstarlist = []
    sigma_vecs = []
    D = set(range(len(vlist)))
    for v in vlist:
        vstar, sigmadict = aug_project_orthogonal(v, vstarlist)
        vstarlist.append(vstar)
        sigma_vecs.append(Vec(D, sigmadict))
    return vstarlist, sigma_vecs


def closest_point(b, vlist):
    """
    Returns b^||V, the point of Span(vlist) closest to b (Computational
    Problem 9.0.4 / Sec 9.4), via the Generalized Fire Engine Lemma 9.1.6:
    b^||V = b - b^perp_V, where b^perp_V comes from orthogonalizing vlist
    first and then projecting b orthogonal to the result.

    >>> from coding_the_matrix.vecutil import list2vec
    >>> vlist = [list2vec([8, -2, 2]), list2vec([4, 2, 4])]
    >>> closest_point(list2vec([5, -5, 2]), vlist) == list2vec([6, -3, 0])
    True
    """
    vstarlist = orthogonalize(vlist)
    return b - project_orthogonal(b, vstarlist)


def find_basis(vlist):
    """
    Returns a basis for Span(vlist) made of the nonzero vectors from
    orthogonalize(vlist) (Sec 9.5.1). By Proposition 9.5.1, mutually
    orthogonal nonzero vectors are automatically linearly independent --
    so filtering out the zero vectors is all that's needed.

    >>> from coding_the_matrix.vecutil import list2vec
    >>> vlist = [list2vec([2, 0, 0]), list2vec([1, 2, 2]), list2vec([3, 2, 2])]
    >>> find_basis(vlist) == [list2vec([2, 0, 0]), list2vec([0, 2, 2])]
    True
    """
    vstarlist = orthogonalize(vlist)
    return [v for v in vstarlist if v * v > ZERO_THRESHOLD]


def find_subset_basis(vlist):
    """
    Returns a basis for Span(vlist) made of ORIGINAL vectors from vlist
    (Sec 9.5.2), rather than the orthogonalized v*. Uses the vi at the same
    positions where orthogonalize(vlist) came out nonzero -- valid because
    project_orthogonal ignores zero vectors already sitting in vstarlist,
    so orthogonalizing just the surviving originals reproduces the same
    vi* at each step.

    >>> from coding_the_matrix.vecutil import list2vec
    >>> vlist = [list2vec([2, 0, 0]), list2vec([1, 2, 2]), list2vec([3, 2, 2])]
    >>> find_subset_basis(vlist) == [list2vec([2, 0, 0]), list2vec([1, 2, 2])]
    True
    """
    vstarlist = orthogonalize(vlist)
    return [vlist[i] for i in range(len(vlist)) if vstarlist[i] * vstarlist[i] > ZERO_THRESHOLD]


def find_orthogonal_complement(U_basis, W_basis):
    """
    Returns a basis for the orthogonal complement of U (given by U_basis)
    with respect to W (given by W_basis) -- Sec 9.6.6. Orthogonalizing
    U_basis + W_basis TOGETHER (U's basis vectors first) makes every
    surviving nonzero w_i* automatically orthogonal to all of U (that's how
    orthogonalize works, each vector gets projected orthogonal to
    everything already accumulated). Exactly dim(W)-dim(U) of them survive
    (Direct-Sum Dimension Corollary 6.3.9), and those are the basis.

    >>> from coding_the_matrix.vecutil import list2vec
    >>> U_basis = [list2vec([8, -2, 2]), list2vec([0, 3, 3])]
    >>> W_basis = [list2vec([1, 0, 0]), list2vec([0, 1, 0]), list2vec([0, 0, 1])]
    >>> basis = find_orthogonal_complement(U_basis, W_basis)
    >>> len(basis) == 1
    True
    >>> approx = [round(x, 3) for x in [basis[0][0], basis[0][1], basis[0][2]]]
    >>> approx == [round(1 / 9, 3), round(2 / 9, 3), round(-2 / 9, 3)]
    True
    """
    vstarlist = orthogonalize(list(U_basis) + list(W_basis))
    return [v for v in vstarlist[len(U_basis):] if v * v > ZERO_THRESHOLD]


# Klein, Sec. 9.7-9.8 -- the QR factorization, A = QR: Q's columns are the
# normalized v* (orthonormal), R is the upper-triangular coefficient matrix
# (Eq 9.7) with each row i scaled by ||vi*|| to compensate for normalizing
# column i (Sec 9.7.3). Requires A's columns to be linearly independent --
# otherwise some vi* is the zero vector and normalizing divides by zero.


def qr_factor(A):
    """
    Returns the QR factorization (Q, R) of Mat A: A == Q*R, Q column-
    orthogonal (Def 9.7.1) with the same column space as A (Lemma 9.7.5), R
    upper-triangular with nonzero diagonal. Requires A's columns to be
    linearly independent.

    >>> from coding_the_matrix.matutil import listlist2mat
    >>> A = listlist2mat([[3, 1], [1, 2]])
    >>> Q, R = qr_factor(A)
    >>> approx_mat_equal(Q * R, A)
    True
    >>> approx_mat_equal(Q.transpose() * Q, Mat(({0, 1}, {0, 1}), {(0, 0): 1, (1, 1): 1}))
    True
    """
    col_labels = sorted(A.D[1], key=str)
    coldict = A.mat2coldict()
    vlist = [coldict[c] for c in col_labels]
    vstarlist, sigma_vecs = aug_orthogonalize(vlist)
    norms = [(v * v) ** 0.5 for v in vstarlist]
    if any(norm * norm <= ZERO_THRESHOLD for norm in norms):
        raise ValueError("qr_factor requires linearly independent columns")

    Q = Mat(
        (A.D[0], set(col_labels)),
        {
            (r, cj): vstarlist[j][r] / norms[j]
            for j, cj in enumerate(col_labels)
            for r in A.D[0]
        },
    )
    R = Mat(
        (set(col_labels), set(col_labels)),
        {
            (ci, cj): sigma_vecs[j][i] * norms[i]
            for j, cj in enumerate(col_labels)
            for i, ci in enumerate(col_labels)
            if sigma_vecs[j][i] * norms[i] != 0
        },
    )
    return Q, R


def QR_solve(A, b):
    """
    Solves Ax=b via the QR factorization (Sec 9.8): substituting A=QR and
    using Q^T*Q=identity reduces Ax=b to the triangular system Rx=Q^T*b,
    solved by backward substitution. If A is square, x is the exact
    solution (Theorem 9.8.1). If A has more rows than columns, x is instead
    the least-squares solution -- the one minimizing ||Ax-b|| (Sec 9.8.5) --
    with no code change needed, same function either way.

    >>> from coding_the_matrix.matutil import listlist2mat
    >>> from coding_the_matrix.vecutil import list2vec
    >>> A = listlist2mat([[3, 1], [1, 2]])
    >>> x = QR_solve(A, list2vec([9, 8]))
    >>> [round(x[0], 6), round(x[1], 6)]
    [2.0, 3.0]

    Least-squares case (Example 9.4.1): A has more rows than columns, so
    Ax=b has no exact solution -- QR_solve returns the x whose A*x is the
    closest point to b in Col(A) (matches closest_point from Sec 9.4).
    >>> A2 = listlist2mat([[8, 4], [-2, 2], [2, 4]])
    >>> b = list2vec([5, -5, 2])
    >>> x2 = QR_solve(A2, b)
    >>> vlist = [list2vec([8, -2, 2]), list2vec([4, 2, 4])]
    >>> approx_equal(A2 * x2, closest_point(b, vlist))
    True
    """
    Q, R = qr_factor(A)
    col_labels = sorted(A.D[1], key=str)
    q_coldict = Q.mat2coldict()
    b_prime = [q_coldict[c] * b for c in col_labels]
    r_rowdict = R.mat2rowdict()
    rowlist = [r_rowdict[c] for c in col_labels]
    return triangular_solve(rowlist, col_labels, b_prime)


def approx_equal(u, v, tol=1e-9):
    """Vec.__eq__ is exact; QR's divisions land results a float epsilon off."""
    assert u.D == v.D
    return all(abs(u[k] - v[k]) < tol for k in u.D)


def approx_mat_equal(A, B, tol=1e-9):
    assert A.D == B.D
    return all(abs(A[r, c] - B[r, c]) < tol for r in A.D[0] for c in A.D[1])
