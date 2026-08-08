from pathlib import Path

import pytest

from coding_the_matrix.mat import Mat
from coding_the_matrix.vec import Vec
from coding_the_matrix.ml_lab import (
    signum, fraction_wrong, loss, find_grad,
    gradient_descent_step, gradient_descent, read_training_data,
)

_DATA_DIR = Path(__file__).parent.parent / "data"


def test_signum_mixed_signs():
    u = Vec({'A', 'B', 'C'}, {'A': 3, 'B': -2, 'C': -0.5})
    assert signum(u) == Vec({'A', 'B', 'C'}, {'A': 1, 'B': -1, 'C': -1})


def test_signum_zero_counts_as_positive():
    u = Vec({'A', 'B'}, {'A': 0, 'B': -0.001})
    assert signum(u) == Vec({'A', 'B'}, {'A': 1, 'B': -1})


def test_signum_preserves_domain():
    u = Vec({'x', 'y', 'z'}, {'x': 5})
    v = signum(u)
    assert v.D == u.D
    assert v == Vec({'x', 'y', 'z'}, {'x': 1, 'y': 1, 'z': 1})  # missing entries are 0 -> +1


def test_signum_all_negative():
    u = Vec({'p', 'q'}, {'p': -7, 'q': -0.01})
    assert signum(u) == Vec({'p', 'q'}, {'p': -1, 'q': -1})


def _toy_dataset():
    # 3 patients, 2 features -- same numbers used in the session's worked example.
    A = Mat(({'p1', 'p2', 'p3'}, {'radius', 'texture'}), {
        ('p1', 'radius'): 2, ('p1', 'texture'): 1,
        ('p2', 'radius'): -1, ('p2', 'texture'): 3,
        ('p3', 'radius'): 0.5, ('p3', 'texture'): -2,
    })
    b = Vec({'p1', 'p2', 'p3'}, {'p1': 1, 'p2': 1, 'p3': -1})
    return A, b


def test_fraction_wrong_perfect_classifier_is_zero():
    A, b = _toy_dataset()
    w = Vec({'radius', 'texture'}, {'radius': 1, 'texture': 1})
    assert fraction_wrong(A, b, w) == 0.0


def test_fraction_wrong_counts_misclassified_patients():
    A, b = _toy_dataset()
    # w = [-1,-1] flips every dot product's sign -> all 3 predictions wrong
    w = Vec({'radius', 'texture'}, {'radius': -1, 'texture': -1})
    assert fraction_wrong(A, b, w) == 1.0


def test_fraction_wrong_partial_misclassification():
    A, b = _toy_dataset()
    # w that only looks at texture: p1=1,p2=3,p3=-2 -> signs [+1,+1,-1] == b, still 0 wrong
    # flip to w=[0,-1] instead: p1=-1,p2=-3,p3=2 -> signs [-1,-1,+1], all 3 wrong vs b=[1,1,-1]
    w = Vec({'radius', 'texture'}, {'radius': 0, 'texture': -1})
    assert fraction_wrong(A, b, w) == 1.0


def test_fraction_wrong_zero_hypothesis_vector():
    # w=0 -> every dot product is 0 -> signum gives +1 for every patient
    A, b = _toy_dataset()
    w = Vec({'radius', 'texture'}, {'radius': 0, 'texture': 0})
    # b = {p1:1, p2:1, p3:-1} -> p1,p2 correct (+1), p3 wrong (predicted +1, actual -1)
    assert fraction_wrong(A, b, w) == 1 / 3


def test_loss_two_patients_two_features():
    # Session's Example 1: A=[q1:[1,2], q2:[3,-1]], b=[-1,1], w=[2,-1] -> L=37
    A = Mat(({'q1', 'q2'}, {'x', 'y'}), {
        ('q1', 'x'): 1, ('q1', 'y'): 2,
        ('q2', 'x'): 3, ('q2', 'y'): -1,
    })
    b = Vec({'q1', 'q2'}, {'q1': -1, 'q2': 1})
    w = Vec({'x', 'y'}, {'x': 2, 'y': -1})
    assert loss(A, b, w) == 37


def test_loss_one_feature_zero_residual_example():
    # Session's Example 2: A=[r1:4, r2:-2, r3:0], b=[1,-1,1], w=[0.5] -> L=2
    # r2's prediction is exactly correct (residual 0), r1 and r3 contribute 1 each.
    A = Mat(({'r1', 'r2', 'r3'}, {'x'}), {
        ('r1', 'x'): 4, ('r2', 'x'): -2, ('r3', 'x'): 0,
    })
    b = Vec({'r1', 'r2', 'r3'}, {'r1': 1, 'r2': -1, 'r3': 1})
    w = Vec({'x'}, {'x': 0.5})
    assert loss(A, b, w) == 2


def test_loss_perfect_classifier_still_nonzero():
    # fraction_wrong is 0 here (right sign for all 3), but loss cares about the
    # raw numeric gap, not just the sign -- so it's still nonzero.
    A, b = _toy_dataset()
    w = Vec({'radius', 'texture'}, {'radius': 1, 'texture': 1})
    assert fraction_wrong(A, b, w) == 0.0
    assert loss(A, b, w) == 5.25


def test_loss_zero_when_predictions_match_exactly():
    A = Mat(({'r1'}, {'x'}), {('r1', 'x'): 4})
    b = Vec({'r1'}, {'r1': 2})
    w = Vec({'x'}, {'x': 0.5})
    assert loss(A, b, w) == 0


def test_find_grad_two_patients_matches_hand_computation():
    # session's transpose walkthrough: A^T*residual=[3,5], grad = 2*[3,5]=[6,10]
    A = Mat(({'p1', 'p2'}, {'radius', 'texture'}), {
        ('p1', 'radius'): 2, ('p1', 'texture'): 1,
        ('p2', 'radius'): -1, ('p2', 'texture'): 3,
    })
    b = Vec({'p1', 'p2'}, {'p1': 1, 'p2': 1})
    w = Vec({'radius', 'texture'}, {'radius': 1, 'texture': 1})
    assert find_grad(A, b, w) == Vec({'radius', 'texture'}, {'radius': 6, 'texture': 10})


def test_find_grad_zero_at_exact_fit():
    # single example, w already fits b exactly -> residual 0 -> gradient is the zero vector
    A = Mat(({'r1'}, {'x'}), {('r1', 'x'): 4})
    b = Vec({'r1'}, {'r1': 2})
    w = Vec({'x'}, {'x': 0.5})
    assert find_grad(A, b, w) == Vec({'x'}, {'x': 0})


def test_find_grad_matches_manual_sum_over_examples():
    # grad L(w) = sum_i 2*(a_i.w - b_i)*a_i -- check against the explicit loop
    # version (not vectorized) on the 3-patient toy dataset.
    A, b = _toy_dataset()
    w = Vec({'radius', 'texture'}, {'radius': 1, 'texture': 1})
    expected = sum(
        (2 * (A.mat2rowdict()[r] * w - b[r])) * A.mat2rowdict()[r] for r in b.D
    )
    assert find_grad(A, b, w) == expected


def test_step_opposite_gradient_reduces_loss():
    # sanity check of the whole point of find_grad: moving a small step in the
    # negative-gradient direction should lower the loss from the current w.
    A, b = _toy_dataset()
    w = Vec({'radius', 'texture'}, {'radius': 1, 'texture': 1})
    grad = find_grad(A, b, w)
    w_next = w + (-0.01) * grad
    assert loss(A, b, w_next) < loss(A, b, w)


def test_gradient_descent_step_matches_manual_formula():
    A, b = _toy_dataset()
    w = Vec({'radius', 'texture'}, {'radius': 1, 'texture': 1})
    sigma = 0.01
    expected = w - sigma * find_grad(A, b, w)
    assert gradient_descent_step(A, b, w, sigma) == expected


def test_gradient_descent_step_overshoots_with_large_sigma():
    # session's numeric demo: sigma=0.01 improves loss, sigma=2.0 makes it explode
    A, b = _toy_dataset()
    w = Vec({'radius', 'texture'}, {'radius': 1, 'texture': 1})
    w_small_step = gradient_descent_step(A, b, w, 0.01)
    w_big_step = gradient_descent_step(A, b, w, 2.0)
    assert loss(A, b, w_small_step) < loss(A, b, w)
    assert loss(A, b, w_big_step) > loss(A, b, w)


def test_gradient_descent_reduces_loss_over_iterations():
    A, b = _toy_dataset()
    w0 = Vec({'radius', 'texture'}, {'radius': 1, 'texture': 1})
    w_final = gradient_descent(A, b, w0, sigma=0.001, T=50)
    assert loss(A, b, w_final) < loss(A, b, w0)


def test_gradient_descent_zero_iterations_returns_initial_w():
    A, b = _toy_dataset()
    w0 = Vec({'radius', 'texture'}, {'radius': 1, 'texture': 1})
    assert gradient_descent(A, b, w0, sigma=0.001, T=0) == w0


@pytest.mark.skipif(
    not (_DATA_DIR / "train.data").exists(),
    reason="WDBC train.data not present locally (gitignored course data)",
)
def test_read_training_data_shape_and_labels():
    A, b = read_training_data(str(_DATA_DIR / "train.data"))
    assert len(b.D) == 300  # data/train.data has 300 patient rows
    assert len(A.D[1]) == 30  # 30 features: 10 params x (mean/stderr/worst)
    assert A.D[0] == b.D  # same patient IDs on both
    assert all(v in (1, -1) for v in b.f.values())
    assert "radius(mean)" in A.D[1]
    assert "fractal dimension(worst)" in A.D[1]


@pytest.mark.skipif(
    not (_DATA_DIR / "train.data").exists(),
    reason="WDBC train.data not present locally (gitignored course data)",
)
def test_gradient_descent_improves_real_dataset_loss():
    A, b = read_training_data(str(_DATA_DIR / "train.data"))
    w0 = Vec(A.D[1], {f: 1 for f in A.D[1]})
    # tiny sigma -- real feature scales (e.g. area ~1000s) make the loss surface
    # much steeper than the toy example, a bigger step would overshoot/explode.
    w_final = gradient_descent(A, b, w0, sigma=1e-9, T=50)
    assert loss(A, b, w_final) < loss(A, b, w0)
