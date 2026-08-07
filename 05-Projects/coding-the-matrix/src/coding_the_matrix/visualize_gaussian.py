"""Interactive step-by-step visualizer for Gaussian elimination — Klein,
"Coding the Matrix", Ch. 7. Walks the FULL process, not just the raw reduction:
pivot selection -> row-addition -> (once all columns are done) the reordered
echelon form -> the results you actually came for (rank, row-space basis,
null-space basis). Same two examples worked by hand in the book: the 5x5
real-number example (Sec. 7.3.2) and the 4x4 GF(2) example (Sec. 7.2) — so you
can see the identical algorithm behave identically over both fields.

Left/Right arrows (or A/D) step through the algorithm one operation at a
time. E switches example. Q closes the window.

Run: uv run python -m coding_the_matrix.visualize_gaussian
"""

from matplotlib import pyplot as plt

from coding_the_matrix.vec import Vec
from coding_the_matrix.vecutil import list2vec, zero_vec
from coding_the_matrix.gf2 import one
from coding_the_matrix.echelon import (
    _gaussian_elimination,
    _col_order,
    row_reduce,
    null_space_basis,
)

# Sec. 7.3.2 — the running example used to introduce M_rowlist tracking.
EXAMPLE_R = [
    list2vec([0, 2, 3, 4, 5]),
    list2vec([0, 0, 0, 3, 2]),
    list2vec([1, 2, 3, 4, 5]),
    list2vec([0, 0, 0, 6, 7]),
    list2vec([0, 0, 0, 9, 8]),
]

# Sec. 7.2 — Gaussian elimination over GF(2), same matrix as the book.
_D_GF2 = {'A', 'B', 'C', 'D'}
EXAMPLE_GF2 = [
    Vec(_D_GF2, {'C': one, 'D': one}),
    Vec(_D_GF2, {'A': one, 'C': one, 'D': one}),
    Vec(_D_GF2, {'A': one, 'C': one}),
    Vec(_D_GF2, {'A': one, 'B': one, 'C': one, 'D': one}),
]

EXAMPLES = {"R": EXAMPLE_R, "GF2": EXAMPLE_GF2}


def _fmt(value):
    if value == 0:
        return "0"
    if value == one:
        return "one"
    if isinstance(value, float):
        return f"{value:.3g}"
    return str(value)


# A "frame" is (kind, rowlist_snapshot, title, detail, pivot_row, target_row).
# kind is "grid" (draw a matrix) or "text" (draw a results panel).


def _explain_pivot(column, pivot_row):
    return (
        f"Columna {column!r}: fila pivot = {pivot_row}",
        f"Fila {pivot_row} es la primera fila que TODAVÍA tiene un valor no-cero en la "
        f"columna {column!r} — se convierte en pivot. De acá en más, cualquier fila con "
        f"algo no-cero en esta columna se va a explicar en función de esta fila.",
    )


def _explain_addition(column, pivot_row, target_row, multiplier):
    return (
        f"Columna {column!r}: fila {target_row} -= {_fmt(multiplier)} * fila {pivot_row}",
        f"Fila {target_row} tenía un valor no-cero en la columna {column!r}. Se lo "
        f"cancelamos restando {_fmt(multiplier)}x la fila pivot ({pivot_row}) — operación "
        f"reversible, no se pierde información, solo se reescribe la fila.",
    )


def _explain_echelon():
    return (
        "Reordenado a echelon form real",
        "Las filas de trabajo (arriba) están indexadas en su posición ORIGINAL, no en el "
        "orden final. echelon_form() las reordena por columna de pivot: esto es lo que "
        "realmente devuelve el algoritmo.",
    )


def _explain_results(rank, m, n):
    dependent = m - rank
    return (
        f"Resultado: rank = {rank} de {m} filas",
        (
            f"{rank} filas son linealmente independientes"
            + (f" ({dependent} fila(s) dependiente(s), quedaron en cero)" if dependent else ", ninguna dependiente, full rank")
            + ". Basis del row space = filas no-cero del echelon form. Basis del null space = filas de M "
            "que corresponden a las filas cero (si las hay) — esas son las combinaciones "
            "que explican por qué esas filas eran redundantes."
        ),
    )


def _build_frames(rowlist):
    """Replay the algorithm and turn it into frames covering the WHOLE
    process: raw reduction -> reordered echelon form -> results summary."""
    D_order = _col_order(rowlist[0].D)
    m, n = len(rowlist), len(D_order)
    record = []
    M, U = _gaussian_elimination(rowlist, record=record)

    frames = [("grid", list(rowlist), "Inicio — matriz de entrada sin tocar",
               "Punto de partida. Vamos a ir columna por columna, de izquierda a "
               "derecha, buscando en cada una un pivot y cancelando el resto.",
               None, None)]

    for step in record:
        if step["kind"] == "pivot":
            title, detail = _explain_pivot(step["column"], step["pivot_row"])
            frames.append(("grid", step["rowlist"], title, detail, step["pivot_row"], None))
        else:
            title, detail = _explain_addition(
                step["column"], step["pivot_row"], step["target_row"], step["multiplier"]
            )
            frames.append(
                ("grid", step["rowlist"], title, detail, step["pivot_row"], step["target_row"])
            )

    title, detail = _explain_echelon()
    frames.append(("grid", U, title, detail, None, None))

    basis = row_reduce(rowlist)
    null_basis = null_space_basis(rowlist)
    title, detail = _explain_results(len(basis), m, n)
    frames.append(("results", (D_order, basis, null_basis), title, detail, None, None))

    return D_order, frames


def _draw_grid(ax, D_order, rowlist, pivot_row, target_row):
    m, n = len(rowlist), len(D_order)
    ax.set_xlim(-0.5, n - 0.5)
    ax.set_ylim(-0.5, m - 0.5)
    ax.invert_yaxis()
    ax.set_xticks(range(n))
    ax.set_xticklabels([str(c) for c in D_order])
    ax.set_yticks(range(m))
    ax.set_yticklabels([f"fila {i}" for i in range(m)])

    for r in range(m):
        if r == pivot_row:
            face = "#8fd19e"  # green — the pivot row this step
        elif r == target_row:
            face = "#f5b971"  # orange — the row being changed this step
        else:
            face = "#eef0f2"
        for c in range(n):
            ax.add_patch(
                plt.Rectangle((c - 0.5, r - 0.5), 1, 1, facecolor=face, edgecolor="white")
            )
            value = rowlist[r][D_order[c]]
            ax.text(c, r, _fmt(value), ha="center", va="center", fontsize=12)


def _draw_results(ax, payload):
    D_order, basis, null_basis = payload
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    lines = [f"Basis del row space ({len(basis)} vector(es)):"]
    for row in basis:
        lines.append("   [" + ", ".join(_fmt(row[c]) for c in D_order) + "]")
    lines.append("")
    lines.append(f"Basis del null space de A^T ({len(null_basis)} vector(es)):")
    if null_basis:
        for u in null_basis:
            lines.append("   [" + ", ".join(_fmt(u[i]) for i in sorted(u.D)) + "]")
    else:
        lines.append("   (vacío — todas las filas son independientes)")

    ax.text(0.02, 0.95, "\n".join(lines), va="top", ha="left", fontsize=12, family="monospace")


def _draw(ax, D_order, frame):
    kind, payload, title, detail, pivot_row, target_row = frame
    ax.clear()
    if kind == "grid":
        _draw_grid(ax, D_order, payload, pivot_row, target_row)
    else:
        _draw_results(ax, payload)
    ax.set_title(title, fontsize=11, pad=10)


def main():
    state = {"example": "R", "frame": 0}
    D_order, frames = _build_frames(EXAMPLES[state["example"]])
    state["D_order"], state["frames"] = D_order, frames

    fig, ax = plt.subplots(figsize=(7.5, 6.3))
    plt.subplots_adjust(bottom=0.22, top=0.88)
    detail_text = fig.text(0.5, 0.10, "", ha="center", va="top", fontsize=9.5, wrap=True)
    fig.text(
        0.5, 0.02,
        "←/→ o A/D: avanzar/retroceder   |   E: cambiar ejemplo (ℝ ↔ GF(2))   |   Q: cerrar",
        ha="center", fontsize=9, color="0.4",
    )

    def redraw():
        frame = state["frames"][state["frame"]]
        _, _, title, detail, _, _ = frame
        full_title = f"[{state['example']}]  step {state['frame']}/{len(state['frames']) - 1}  —  {title}"
        _draw(ax, state["D_order"], (frame[0], frame[1], full_title, detail, frame[4], frame[5]))
        detail_text.set_text(detail)
        fig.canvas.draw_idle()

    def on_key(event):
        if event.key in ("right", "d"):
            state["frame"] = min(state["frame"] + 1, len(state["frames"]) - 1)
        elif event.key in ("left", "a"):
            state["frame"] = max(state["frame"] - 1, 0)
        elif event.key == "e":
            state["example"] = "GF2" if state["example"] == "R" else "R"
            D_order, frames = _build_frames(EXAMPLES[state["example"]])
            state["D_order"], state["frames"], state["frame"] = D_order, frames, 0
        elif event.key == "q":
            plt.close(fig)
            return
        redraw()

    fig.canvas.mpl_connect("key_press_event", on_key)
    redraw()
    plt.show()


if __name__ == "__main__":
    main()
