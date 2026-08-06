"""Interactive 2D eigenvector visualizer — sliders for a,b,c,d of
[[a,b],[c,d]], live-redraws the transformed grid + eigenvector spans,
same idea as the 3B1B "vector knocked off span" vs "stays on its span" frames.

Run: uv run python -m eigenvectors_3b1b.visualize
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider

GRID_RANGE = range(-4, 5)
SPAN_T = np.linspace(-5, 5, 2)


def eigen_real_directions(A: np.ndarray) -> list[tuple[np.ndarray, float]]:
    """Real (eigenvector, eigenvalue) pairs only — complex ones (pure
    rotation-like matrices) have no line that stays on its own span."""
    eigenvalues, eigenvectors = np.linalg.eig(A)
    pairs = []
    for i in range(len(eigenvalues)):
        if np.isreal(eigenvalues[i]):
            pairs.append((eigenvectors[:, i].real, eigenvalues[i].real))
    return pairs


def transformed_grid_lines(A: np.ndarray):
    lines = []
    for x in GRID_RANGE:
        pts = np.array([[x, y] for y in np.linspace(-5, 5, 50)]).T
        lines.append(A @ pts)
    for y in GRID_RANGE:
        pts = np.array([[x, y] for x in np.linspace(-5, 5, 50)]).T
        lines.append(A @ pts)
    return lines


def main():
    fig, ax = plt.subplots(figsize=(7, 7))
    plt.subplots_adjust(bottom=0.32)
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_aspect("equal")
    ax.axhline(0, color="0.7", lw=0.8)
    ax.axvline(0, color="0.7", lw=0.8)

    slider_axes = [plt.axes([0.25, 0.20 - 0.05 * i, 0.55, 0.03]) for i in range(4)]
    labels = ["a", "b", "c", "d"]
    initial = [3.0, 1.0, 0.0, 2.0]
    sliders = [
        Slider(slider_axes[i], labels[i], -3.0, 3.0, valinit=initial[i])
        for i in range(4)
    ]

    def redraw(_event=None):
        ax.clear()
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.set_aspect("equal")
        ax.axhline(0, color="0.7", lw=0.8)
        ax.axvline(0, color="0.7", lw=0.8)

        a, b, c, d = (s.val for s in sliders)
        A = np.array([[a, b], [c, d]])

        for line in transformed_grid_lines(A):
            ax.plot(line[0], line[1], color="steelblue", lw=0.5, alpha=0.5)

        for vec, color, label in [((1, 0), "green", "î"), ((0, 1), "crimson", "ĵ")]:
            tv = A @ np.array(vec)
            ax.annotate(
                "", xy=tv, xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color=color, lw=2),
            )
            ax.text(*tv, f" {label}'", color=color)

        eig_pairs = eigen_real_directions(A)
        eig_colors = ["darkorange", "purple"]
        for (vec, val), color in zip(eig_pairs, eig_colors):
            unit = vec / np.linalg.norm(vec)
            span = np.outer(unit, SPAN_T)
            ax.plot(span[0], span[1], color=color, lw=1.5, ls="--",
                     label=f"span λ={val:.2f}")
            ax.annotate(
                "", xy=A @ unit, xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color=color, lw=2.5),
            )

        title = "Eigenvector spans (líneas punteadas) — quedan fijas bajo la transformación"
        if not eig_pairs:
            title = "Sin autovectores reales — todo vector rota fuera de su span"
        ax.set_title(title, fontsize=10)
        if eig_pairs:
            ax.legend(loc="upper left", fontsize=8)
        fig.canvas.draw_idle()

    for s in sliders:
        s.on_changed(redraw)

    redraw()
    plt.show()


if __name__ == "__main__":
    main()
