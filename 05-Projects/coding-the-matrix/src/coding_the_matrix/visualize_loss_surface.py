"""3D loss-surface visualizer -- Klein, "Coding the Matrix", Sec 8.4.5's
hill-climbing illustration (the inverted-paraboloid "valley"), but drawn from
REAL WDBC data instead of an illustrative sketch. L(w) can only be plotted
for a 2-weight hypothesis vector (w1, w2 -> height = 3rd dimension; the real
30-feature problem would need 31 dimensions, undrawable) -- so this reuses
the same 2 toy features (radius(mean), texture(mean)) as
visualize_ml_lab.py's decision-boundary panel, showing the OTHER half of the
same story: not what the line looks like, but the bowl gradient descent is
actually walking down to find it.

Interactive: the surface is fixed, and Left/Right (or A/D) step the descent
marker one recorded checkpoint at a time down toward the base of the valley
-- same key-navigation pattern as visualize_gaussian.py. Mouse-drag still
rotates the view at any step. Q closes.

Run: uv run python -m coding_the_matrix.visualize_loss_surface
"""
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt

from coding_the_matrix.mat import Mat
from coding_the_matrix.vec import Vec
from coding_the_matrix.ml_lab import read_training_data, loss, gradient_descent_step

_DATA_DIR = Path(__file__).parent.parent.parent / "data"
_FEATURES = ["radius(mean)", "texture(mean)"]
_W_RANGE = (-0.35, 0.35)
_GRID_N = 45
_SIGMA, _T = 1e-6, 2900
# starting point chosen high up the (safe) opposite-sign diagonal of the valley
# -- w0=(0,0) is already almost at the minimum (L=300 vs L*=277), barely a hill
# to descend. This starts at L~1009 and converges to the same true minimum
# (L*=277.39 at w*=(0.072,-0.049)) after the same T iterations, so the path
# is visibly longer/steeper instead of a near-flat two-point line.
_W0 = {"radius(mean)": 0.25, "texture(mean)": -0.25}
_N_FRAMES = 30  # checkpoints along the descent path, evenly spaced in iterations
# radius(mean) and texture(mean) are positively correlated across patients, so
# same-sign weights amplify predictions wildly (L up to ~44,000 at the grid
# corners) while opposite-sign weights stay bounded -- an elongated, narrow
# valley, not a symmetric bowl. Clipping the z-axis keeps that shallow valley
# floor (L ~ 270-300) visible instead of it getting flattened by those walls.
_Z_CLIP = 1200


def _project(A, features):
    rows = A.mat2rowdict()
    D = set(features)
    return Mat((A.D[0], D), {(r, f): rows[r][f] for r in A.D[0] for f in D})


def _run_descent_path(A, b, w0, sigma, T, n_frames):
    fx, fy = _FEATURES
    checkpoint_every = max(T // n_frames, 1)
    path = [{"t": 0, "w1": w0[fx], "w2": w0[fy], "loss": loss(A, b, w0)}]
    w = w0
    for t in range(1, T + 1):
        w = gradient_descent_step(A, b, w, sigma)
        if t % checkpoint_every == 0 or t == T:
            path.append({"t": t, "w1": w[fx], "w2": w[fy], "loss": loss(A, b, w)})
            if len(path) >= n_frames:
                break
    return path


def main():
    print("Cargando WDBC train.data...")
    A_train, b_train = read_training_data(str(_DATA_DIR / "train.data"))
    A2 = _project(A_train, _FEATURES)
    fx, fy = _FEATURES

    print(f"Corriendo gradient descent (sigma={_SIGMA}, T={_T}) para trazar el camino...")
    w0 = Vec(set(_FEATURES), _W0)
    path = _run_descent_path(A2, b_train, w0, _SIGMA, _T, _N_FRAMES)
    n_frames = len(path)

    print(f"Evaluando L(w) en grilla {_GRID_N}x{_GRID_N}...")
    w1_vals = np.linspace(*_W_RANGE, _GRID_N)
    w2_vals = np.linspace(*_W_RANGE, _GRID_N)
    W1, W2 = np.meshgrid(w1_vals, w2_vals)
    Z = np.empty_like(W1)
    for i in range(_GRID_N):
        for j in range(_GRID_N):
            w = Vec(set(_FEATURES), {fx: W1[i, j], fy: W2[i, j]})
            Z[i, j] = loss(A2, b_train, w)

    state = {"frame": 0}
    fig = plt.figure(figsize=(9, 7.5))
    ax = fig.add_subplot(111, projection="3d")
    fig.text(
        0.5, 0.05,
        "←/→ o A/D: avanzar/retroceder paso   |   mouse: rotar vista   |   Q: cerrar",
        ha="center", fontsize=9, color="0.4",
    )
    fig.text(
        0.5, 0.015,
        f"valle angosto (radius y texture correlacionados) -- las 2 esquinas del mismo signo "
        f"llegan a L~44,000, recortadas en {_Z_CLIP} para no aplastar el piso real.",
        ha="center", fontsize=8, color="0.5",
    )

    def redraw():
        i = state["frame"]
        ax.clear()
        Z_clipped = np.minimum(Z, _Z_CLIP)  # flatten the runaway corners so the
        ax.plot_surface(W1, W2, Z_clipped, cmap="viridis", alpha=0.6, edgecolor="none")

        so_far = path[: i + 1]
        xs = [p["w1"] for p in so_far]
        ys = [p["w2"] for p in so_far]
        zs = [p["loss"] for p in so_far]
        ax.plot(xs, ys, zs, color="red", marker="o", markersize=3, linewidth=2)
        ax.scatter([xs[0]], [ys[0]], [zs[0]], color="black", s=50,
                   label=f"inicio w=({xs[0]:.2f},{ys[0]:.2f})  L={zs[0]:.0f}")
        ax.scatter([xs[-1]], [ys[-1]], [zs[-1]], color="lime", s=70,
                   label=f"iter {so_far[-1]['t']}  L={zs[-1]:.1f}  (posición actual)")

        ax.set_zlim(0, _Z_CLIP)
        ax.set_xlabel(f"w[{fx}]")
        ax.set_ylabel(f"w[{fy}]")
        ax.set_zlabel(f"L(w)  (recortado a {_Z_CLIP}, ver nota abajo)")
        ax.set_title(
            f"paso {i}/{n_frames - 1}  —  L(w) = ||Aw-b||^2 (radius, texture reales)\n"
            f"iter {so_far[-1]['t']}/{_T}   L={zs[-1]:.1f}"
        )
        ax.legend(fontsize=8, loc="upper left")
        fig.canvas.draw_idle()

    def on_key(event):
        if event.key in ("right", "d"):
            state["frame"] = min(state["frame"] + 1, n_frames - 1)
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
