"""Interactive step-by-step 3D visualizer for Gram-Schmidt orthogonalization
(Klein, "Coding the Matrix", Ch. 9, orthogonalize()) -- Klein's own running
example 9.3.2: v1=[2,0,0], v2=[1,2,2], v3=[1,0,2].

Walks the SAME sequence of projections orthogonalize() does internally, one
projection/subtraction at a time, in 3D: original vectors (gray), the
running v*'s already found (green, solid), the vector currently being
processed (blue), the projection about to be subtracted (dashed orange),
and the result once subtracted.

Left/Right arrows (or A/D) step through. Q closes the window.

Run: uv run python -m coding_the_matrix.visualize_orthogonalize
"""
from matplotlib import pyplot as plt

from coding_the_matrix.vecutil import list2vec
from coding_the_matrix.orthogonalization import project_along, project_orthogonal_1

V1 = list2vec([2, 0, 0])
V2 = list2vec([1, 2, 2])
V3 = list2vec([1, 0, 2])
VLIST = [V1, V2, V3]


def _xyz(v):
    return v[0], v[1], v[2]


def _fmt(v):
    return f"[{v[0]:.3g}, {v[1]:.3g}, {v[2]:.3g}]"


def _dot(u, v):
    return u * v


def _build_frames():
    """Replays orthogonalize(VLIST) step by step, recording enough state at
    each projection/subtraction to draw it. A "frame" is a dict of named
    3-vectors to draw plus title/detail text -- mirrors the (kind, payload,
    title, detail, ...) tuple pattern of visualize_gaussian.py."""
    frames = []

    frames.append({
        "vectors": {"v1": (V1, "0.6"), "v2": (V2, "0.6"), "v3": (V3, "0.6")},
        "title": "Vectores originales -- v1, v2, v3 (Ejemplo 9.3.2)",
        "detail": (
            f"v1={_fmt(V1)}, v2={_fmt(V2)}, v3={_fmt(V3)}. Ninguno es ortogonal a "
            "los otros todavia -- vamos a correr Gram-Schmidt (orthogonalize) para "
            "construir v1*, v2*, v3* mutuamente ortogonales con el MISMO span."
        ),
    })

    # --- v1: nothing to project against, v1* = v1 ---
    v1_star = V1
    frames.append({
        "vectors": {"v1*": (v1_star, "#2ca02c"), "v2": (V2, "0.6"), "v3": (V3, "0.6")},
        "title": "Paso 1 -- v1* = v1 (lista vacia, nada que restar)",
        "detail": f"v1* = {_fmt(v1_star)}. Primer vector de vstarlist: se copia tal cual.",
    })

    # --- v2: project onto v1*, subtract ---
    proj_v2_v1 = project_along(V2, v1_star)
    frames.append({
        "vectors": {
            "v1*": (v1_star, "#2ca02c"), "v2": (V2, "#1f77b4"), "v3": (V3, "0.6"),
            "proj(v2,v1*)": (proj_v2_v1, "--#ff7f0e"),
        },
        "title": "Paso 2a -- proyectar v2 sobre v1*",
        "detail": (
            f"sigma = <v2,v1*>/<v1*,v1*> = {_dot(V2, v1_star)}/{_dot(v1_star, v1_star)} "
            f"= {_dot(V2, v1_star) / _dot(v1_star, v1_star):.3g}. "
            f"proj = sigma*v1* = {_fmt(proj_v2_v1)} (flecha punteada, sobre la direccion de v1*)."
        ),
    })
    v2_star = project_orthogonal_1(V2, v1_star)
    frames.append({
        "vectors": {"v1*": (v1_star, "#2ca02c"), "v2*": (v2_star, "#2ca02c"), "v3": (V3, "0.6")},
        "title": "Paso 2b -- v2* = v2 - proj(v2,v1*)",
        "detail": (
            f"v2* = {_fmt(v2_star)}. Chequeo: <v2*,v1*> = {_dot(v2_star, v1_star):.3g} "
            "(0 -- ortogonal a v1*, como debe ser)."
        ),
    })

    # --- v3: project onto v1*, subtract; then project onto v2*, subtract ---
    proj_v3_v1 = project_along(V3, v1_star)
    frames.append({
        "vectors": {
            "v1*": (v1_star, "#2ca02c"), "v2*": (v2_star, "#2ca02c"),
            "v3": (V3, "#1f77b4"), "proj(v3,v1*)": (proj_v3_v1, "--#ff7f0e"),
        },
        "title": "Paso 3a -- proyectar v3 sobre v1*",
        "detail": (
            f"sigma = {_dot(V3, v1_star)}/{_dot(v1_star, v1_star)} "
            f"= {_dot(V3, v1_star) / _dot(v1_star, v1_star):.3g}. "
            f"proj = {_fmt(proj_v3_v1)}."
        ),
    })
    v3_a = project_orthogonal_1(V3, v1_star)
    frames.append({
        "vectors": {
            "v1*": (v1_star, "#2ca02c"), "v2*": (v2_star, "#2ca02c"),
            "v3_a": (v3_a, "#1f77b4"),
        },
        "title": "Paso 3b -- v3_a = v3 - proj(v3,v1*)",
        "detail": (
            f"v3_a = {_fmt(v3_a)} -- ya ortogonal a v1* "
            f"(<v3_a,v1*>={_dot(v3_a, v1_star):.3g}), pero todavia NO a v2*."
        ),
    })
    proj_v3a_v2 = project_along(v3_a, v2_star)
    frames.append({
        "vectors": {
            "v1*": (v1_star, "#2ca02c"), "v2*": (v2_star, "#2ca02c"),
            "v3_a": (v3_a, "#1f77b4"), "proj(v3_a,v2*)": (proj_v3a_v2, "--#ff7f0e"),
        },
        "title": "Paso 3c -- proyectar v3_a sobre v2*",
        "detail": (
            f"sigma = {_dot(v3_a, v2_star)}/{_dot(v2_star, v2_star)} "
            f"= {_dot(v3_a, v2_star) / _dot(v2_star, v2_star):.3g}. "
            f"proj = {_fmt(proj_v3a_v2)}. Restando esto NO reintroduce componente en v1* "
            "porque v2* ya es ortogonal a v1* (Sec 9.2, Example 9.2.1)."
        ),
    })
    v3_star = project_orthogonal_1(v3_a, v2_star)
    frames.append({
        "vectors": {"v1*": (v1_star, "#2ca02c"), "v2*": (v2_star, "#2ca02c"), "v3*": (v3_star, "#2ca02c")},
        "title": "Paso 3d -- v3* = v3_a - proj(v3_a,v2*)",
        "detail": f"v3* = {_fmt(v3_star)}.",
    })

    frames.append({
        "vectors": {"v1*": (v1_star, "#2ca02c"), "v2*": (v2_star, "#2ca02c"), "v3*": (v3_star, "#2ca02c")},
        "title": "Resultado -- v1*, v2*, v3* mutuamente ortogonales",
        "detail": (
            f"<v1*,v2*>={_dot(v1_star, v2_star):.3g}  <v1*,v3*>={_dot(v1_star, v3_star):.3g}  "
            f"<v2*,v3*>={_dot(v2_star, v3_star):.3g} -- los tres dan 0. "
            "Span{v1*,v2*,v3*} = Span{v1,v2,v3} (Lemma 9.3.5) -- mismo espacio, base limpia."
        ),
    })

    return frames


def _draw(ax, frame):
    ax.clear()
    all_pts = []
    for name, spec in frame["vectors"].items():
        vec, color = spec
        dashed = isinstance(color, str) and color.startswith("--")
        if dashed:
            color = color[2:]
        x, y, z = _xyz(vec)
        all_pts.append((x, y, z))
        ax.quiver(
            0, 0, 0, x, y, z,
            color=color, linestyle="--" if dashed else "-",
            linewidth=2, arrow_length_ratio=0.12,
        )
        ax.text(x * 1.08, y * 1.08, z * 1.08, name, fontsize=10, color=color if not dashed else "#b35900")

    limit = max(3.0, max((abs(c) for pt in all_pts for c in pt), default=3.0) * 1.3)
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_zlim(-limit, limit)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_title(frame["title"], fontsize=11, pad=10)


def main():
    frames = _build_frames()
    state = {"frame": 0}

    fig = plt.figure(figsize=(8, 7.5))
    ax = fig.add_subplot(111, projection="3d")
    plt.subplots_adjust(bottom=0.22, top=0.90)
    detail_text = fig.text(0.5, 0.09, "", ha="center", va="top", fontsize=9, wrap=True)
    fig.text(
        0.5, 0.02,
        "←/→ o A/D: avanzar/retroceder   |   Q: cerrar",
        ha="center", fontsize=9, color="0.4",
    )

    def redraw():
        frame = frames[state["frame"]]
        _draw(ax, frame)
        ax.set_title(f"step {state['frame']}/{len(frames) - 1}  —  {frame['title']}", fontsize=10, pad=10)
        detail_text.set_text(frame["detail"])
        fig.canvas.draw_idle()

    def on_key(event):
        if event.key in ("right", "d"):
            state["frame"] = min(state["frame"] + 1, len(frames) - 1)
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
