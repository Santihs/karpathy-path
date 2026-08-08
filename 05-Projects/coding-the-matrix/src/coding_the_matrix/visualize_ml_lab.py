"""Interactive step-by-step visualizer for the Ch. 8.4 machine-learning lab
(Klein, "Coding the Matrix") -- gradient descent training a linear classifier
on the WDBC breast-cancer dataset.

Two things happening side by side as you step through iterations:
 - left/middle: loss and fraction_wrong curves (train vs validate) for the
   REAL 30-feature classifier, revealed progressively -- this is what you'd
   actually watch during training.
 - right: a toy 2-feature version (radius(mean), texture(mean) only) so the
   decision boundary (w.x = 0, a literal line) is drawable -- watch it rotate
   into place as gradient descent runs. The real 30D boundary can't be drawn
   (30 dimensions), this is a stand-in for intuition, same 2 features used
   as the toy examples earlier in this chapter's notes.

Left/Right arrows (or A/D) step through checkpoints. Q closes the window.
Requires data/train.data and data/validate.data (gitignored WDBC files,
see 02-Topics/Coding-the-Matrix-Inner-Product.md for where to get them).

Run: uv run python -m coding_the_matrix.visualize_ml_lab
"""
from pathlib import Path

from matplotlib import pyplot as plt

from coding_the_matrix.mat import Mat
from coding_the_matrix.vec import Vec
from coding_the_matrix.ml_lab import (
    read_training_data, gradient_descent_step, loss, fraction_wrong,
)

_DATA_DIR = Path(__file__).parent.parent.parent / "data"
_N_FRAMES = 30
_REAL_SIGMA, _REAL_T = 1e-9, 9000
_TOY_SIGMA, _TOY_T = 1e-6, 2900
_TOY_FEATURES = ["radius(mean)", "texture(mean)"]


def _record_checkpoints(A, b, w0, sigma, T, n_frames, extra_eval=None):
    """Runs gradient descent for T steps, snapshotting w (and loss/fraction_wrong,
    plus an optional extra dataset's loss/fraction_wrong) at n_frames evenly
    spaced points -- so scrubbing through frames later doesn't need to retrain."""
    checkpoint_every = max(T // n_frames, 1)
    checkpoints = []
    w = w0
    for t in range(T + 1):
        if t % checkpoint_every == 0 or t == T:
            row = {"t": t, "w": w, "loss": loss(A, b, w), "fw": fraction_wrong(A, b, w)}
            if extra_eval is not None:
                A2, b2 = extra_eval
                row["loss2"] = loss(A2, b2, w)
                row["fw2"] = fraction_wrong(A2, b2, w)
            checkpoints.append(row)
            if len(checkpoints) >= n_frames:
                break
        w = gradient_descent_step(A, b, w, sigma)
    return checkpoints


def _project(A, features):
    rows = A.mat2rowdict()
    D = set(features)
    return Mat((A.D[0], D), {(r, f): rows[r][f] for r in A.D[0] for f in D})


def _boundary_points(w, xlim):
    # w.x = 0  ->  w[fx]*x + w[fy]*y = 0  ->  y = -(w[fx]/w[fy]) * x
    fx, fy = _TOY_FEATURES
    if abs(w[fy]) < 1e-12:
        return None
    x0, x1 = xlim
    return [x0, x1], [-(w[fx] / w[fy]) * x0, -(w[fx] / w[fy]) * x1]


def _draw(fig, axes, real_ckpts, toy_ckpts, toy_points, frame):
    ax_loss, ax_fw, ax_scatter = axes
    i = min(frame, len(real_ckpts) - 1)
    j = min(frame, len(toy_ckpts) - 1)
    real_so_far = real_ckpts[: i + 1]
    toy_ck = toy_ckpts[j]

    ax_loss.clear()
    ts = [c["t"] for c in real_so_far]
    ax_loss.plot(ts, [c["loss"] for c in real_so_far], "o-", color="#2b6cb0", label="train")
    ax_loss.plot(ts, [c["loss2"] for c in real_so_far], "o-", color="#e07b39", label="validate")
    ax_loss.set_yscale("log")
    ax_loss.set_xlabel("iteración")
    ax_loss.set_title("loss (30 features, escala log)")
    ax_loss.legend(fontsize=8)

    ax_fw.clear()
    ax_fw.plot(ts, [c["fw"] for c in real_so_far], "o-", color="#2b6cb0", label="train")
    ax_fw.plot(ts, [c["fw2"] for c in real_so_far], "o-", color="#e07b39", label="validate")
    ax_fw.set_ylim(-0.02, 0.6)
    ax_fw.set_xlabel("iteración")
    ax_fw.set_title("fraction_wrong (30 features)")
    ax_fw.legend(fontsize=8)

    ax_scatter.clear()
    xs, ys, colors = toy_points
    ax_scatter.scatter(xs, ys, c=colors, s=14, alpha=0.6)
    xlim = (min(xs) - 1, max(xs) + 1)
    ax_scatter.set_xlim(*xlim)
    ax_scatter.set_ylim(min(ys) - 2, max(ys) + 2)
    line = _boundary_points(toy_ck["w"], xlim)
    if line:
        ax_scatter.plot(line[0], line[1], color="black", linewidth=2)
    ax_scatter.set_xlabel(_TOY_FEATURES[0])
    ax_scatter.set_ylabel(_TOY_FEATURES[1])
    ax_scatter.set_title(
        f"frontera de decisión (2 features)\niter {toy_ck['t']}  fw={toy_ck['fw']:.2f}"
    )

    fig.suptitle(
        f"paso {frame}/{_N_FRAMES - 1}  —  30D: iter {real_so_far[-1]['t']}  "
        f"loss_train={real_so_far[-1]['loss']:.1f}  fw_val={real_so_far[-1]['fw2']:.3f}",
        fontsize=11,
    )
    fig.canvas.draw_idle()


def main():
    print("Cargando WDBC train/validate.data...")
    A_train, b_train = read_training_data(str(_DATA_DIR / "train.data"))
    A_val, b_val = read_training_data(str(_DATA_DIR / "validate.data"))

    print(f"Entrenando clasificador real (30 features, sigma={_REAL_SIGMA}, T={_REAL_T})...")
    w0_real = Vec(A_train.D[1], {f: 0 for f in A_train.D[1]})
    real_ckpts = _record_checkpoints(
        A_train, b_train, w0_real, _REAL_SIGMA, _REAL_T, _N_FRAMES, extra_eval=(A_val, b_val)
    )

    print(f"Entrenando toy de 2 features (sigma={_TOY_SIGMA}, T={_TOY_T})...")
    A_toy = _project(A_train, _TOY_FEATURES)
    w0_toy = Vec(set(_TOY_FEATURES), {f: 0 for f in _TOY_FEATURES})
    toy_ckpts = _record_checkpoints(A_toy, b_train, w0_toy, _TOY_SIGMA, _TOY_T, _N_FRAMES)

    rows = A_toy.mat2rowdict()
    fx, fy = _TOY_FEATURES
    xs = [rows[r][fx] for r in A_toy.D[0]]
    ys = [rows[r][fy] for r in A_toy.D[0]]
    colors = ["#c0392b" if b_train[r] == 1 else "#2980b9" for r in A_toy.D[0]]
    toy_points = (xs, ys, colors)

    state = {"frame": 0}
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    plt.subplots_adjust(bottom=0.15, top=0.82, wspace=0.35)
    fig.text(
        0.5, 0.02,
        "←/→ o A/D: avanzar/retroceder   |   Q: cerrar   |   rojo=malignant azul=benign",
        ha="center", fontsize=9, color="0.4",
    )

    def redraw():
        _draw(fig, axes, real_ckpts, toy_ckpts, toy_points, state["frame"])

    def on_key(event):
        if event.key in ("right", "d"):
            state["frame"] = min(state["frame"] + 1, _N_FRAMES - 1)
        elif event.key in ("left", "a"):
            state["frame"] = max(state["frame"] - 1, 0)
        elif event.key == "q":
            plt.close(fig)
            return
        redraw()

    fig.canvas.mpl_connect("key_press_event", on_key)
    redraw()
    plt.show()


if __name__ == "__main__":
    main()
