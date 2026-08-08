# Klein, "Coding the Matrix", Ch. 8.4 -- Lab: machine learning (WDBC breast
# cancer classifier). The hypothesis class is linear functions h(y) = w.y;
# C(y) = sign(h(y)) decides malignant (+1) vs benign (-1). signum() is the
# elementwise building block fraction_wrong() will use to score a hypothesis
# vector w against labeled examples.
#
# read_training_data() is our own parser for the WDBC data files (Sec 8.4.1
# format), not a copy of the course-provided cancer_data.py -- that file is
# copyrighted course material we deliberately didn't bring into this (public)
# repo, same reasoning as data/.gitignore for train.data/validate.data.
from coding_the_matrix.vec import Vec
from coding_the_matrix.matutil import rowdict2mat

_FEATURE_PARAMS = [
    "radius", "texture", "perimeter", "area", "smoothness",
    "compactness", "concavity", "concave points", "symmetry", "fractal dimension",
]
_FEATURE_STATS = ["(mean)", "(stderr)", "(worst)"]


def read_training_data(fname):
    """
    Reads a WDBC data file (Sec 8.4.1: "patient_id,diagnosis,30 features..."
    per line, features in mean/stderr/worst blocks of 10) and returns (A, b):
    A is a Mat with row labels = patient IDs, column labels = the 30 feature
    name strings; b is a Vec with domain = patient IDs, +1 if malignant
    ('M'), -1 if benign ('B').
    """
    feature_vectors = {}
    diagnoses = {}
    with open(fname) as f:
        for line in f:
            fields = line.strip().split(",")
            patient_id = int(fields[0])
            diagnoses[patient_id] = 1 if fields[1] == "M" else -1
            values = {
                f"{param}{stat}": float(fields[2 + stat_idx * len(_FEATURE_PARAMS) + param_idx])
                for stat_idx, stat in enumerate(_FEATURE_STATS)
                for param_idx, param in enumerate(_FEATURE_PARAMS)
            }
            feature_vectors[patient_id] = Vec(set(values), values)
    return rowdict2mat(feature_vectors), Vec(set(diagnoses), diagnoses)


def signum(u):
    """
    Returns the Vec v with the same domain as u such that v[d] is +1 if
    u[d] >= 0, else -1 (Task 8.4.2).

    >>> signum(Vec({'A', 'B'}, {'A': 3, 'B': -2})) == Vec({'A', 'B'}, {'A': 1, 'B': -1})
    True
    >>> signum(Vec({'A', 'B'}, {'A': 0, 'B': -0.001})) == Vec({'A', 'B'}, {'A': 1, 'B': -1})
    True
    """
    return Vec(u.D, {d: (1 if u[d] >= 0 else -1) for d in u.D})


def fraction_wrong(A, b, w):
    """
    Returns the fraction of row labels r of A such that the sign of
    (row r of A).w differs from b[r] (Task 8.4.3). A's rows are feature
    vectors, b's entries are +1/-1 labels, w is a hypothesis vector.

    >>> from coding_the_matrix.mat import Mat
    >>> A = Mat(({'p1','p2','p3'}, {'radius','texture'}), {
    ...     ('p1','radius'): 2, ('p1','texture'): 1,
    ...     ('p2','radius'): -1, ('p2','texture'): 3,
    ...     ('p3','radius'): 0.5, ('p3','texture'): -2,
    ... })
    >>> b = Vec({'p1','p2','p3'}, {'p1': 1, 'p2': 1, 'p3': -1})
    >>> w = Vec({'radius','texture'}, {'radius': 1, 'texture': 1})
    >>> fraction_wrong(A, b, w)
    0.0
    """
    predicted = signum(A * w)
    wrong = sum(1 for r in b.D if predicted[r] != b[r])
    return wrong / len(b.D)


def loss(A, b, w):
    """
    Returns L(w) = ||Aw - b||^2, the sum-of-squared-errors loss on training
    data A, b for hypothesis vector w (Task 8.4.4). Unlike fraction_wrong,
    this is smooth/differentiable -- what gradient descent actually minimizes.

    >>> from coding_the_matrix.mat import Mat
    >>> A = Mat(({'r1','r2','r3'}, {'x'}), {('r1','x'): 4, ('r2','x'): -2, ('r3','x'): 0})
    >>> b = Vec({'r1','r2','r3'}, {'r1': 1, 'r2': -1, 'r3': 1})
    >>> loss(A, b, Vec({'x'}, {'x': 0.5}))
    2.0
    """
    residual = A * w - b
    return residual * residual


def find_grad(A, b, w):
    """
    Returns the gradient of L at w (Task 8.4.9), grad L(w) = sum_i
    2*(a_i.w - b_i)*a_i (Equation 8.9) -- the direction of steepest ascent
    of the loss from this point; gradient descent moves opposite to it.

    >>> from coding_the_matrix.mat import Mat
    >>> A = Mat(({'p1','p2'}, {'radius','texture'}), {
    ...     ('p1','radius'): 2, ('p1','texture'): 1,
    ...     ('p2','radius'): -1, ('p2','texture'): 3,
    ... })
    >>> b = Vec({'p1','p2'}, {'p1': 1, 'p2': 1})
    >>> w = Vec({'radius','texture'}, {'radius': 1, 'texture': 1})
    >>> find_grad(A, b, w) == Vec({'radius','texture'}, {'radius': 6, 'texture': 10})
    True
    """
    residual = A * w - b
    return 2 * (A.transpose() * residual)


def gradient_descent_step(A, b, w, sigma):
    """
    Returns the next hypothesis vector (Task 8.4.10): w minus sigma times
    the gradient of L at w. Subtraction, not addition -- the gradient points
    toward steepest ascent, so minimizing means moving the opposite way.

    >>> from coding_the_matrix.mat import Mat
    >>> A = Mat(({'p1','p2'}, {'radius','texture'}), {
    ...     ('p1','radius'): 2, ('p1','texture'): 1,
    ...     ('p2','radius'): -1, ('p2','texture'): 3,
    ... })
    >>> b = Vec({'p1','p2'}, {'p1': 1, 'p2': 1})
    >>> w = Vec({'radius','texture'}, {'radius': 1, 'texture': 1})
    >>> w_next = gradient_descent_step(A, b, w, 0.01)
    >>> abs(w_next['radius'] - 0.94) < 1e-9 and abs(w_next['texture'] - 0.9) < 1e-9
    True
    """
    return w - sigma * find_grad(A, b, w)


def gradient_descent(A, b, w, sigma, T, verbose=False):
    """
    Runs gradient_descent_step for T iterations starting from w, returning
    the final hypothesis vector (Task 8.4.11). If verbose, prints loss and
    fraction_wrong every 30 iterations to watch training progress.
    """
    for t in range(T):
        if verbose and t % 30 == 0:
            print(f"iter {t}: loss={loss(A, b, w)} fraction_wrong={fraction_wrong(A, b, w)}")
        w = gradient_descent_step(A, b, w, sigma)
    return w
