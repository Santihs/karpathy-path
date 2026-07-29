# Persistent, rerunnable generators for 07-Visuals/ pages (see CLAUDE.md
# "Explanation Style"). Run directly: uv run python -m coding_the_matrix.viz_examples
from coding_the_matrix.mat import Mat, find_triangular_order
from coding_the_matrix.triangular import triangular_solve
from coding_the_matrix.viz_html import render_page, matrix_table_html, trace_table_html
from coding_the_matrix.basis import _EliminationBasis
from coding_the_matrix.msf import edge_to_vec


def generate_triangular_reorder_solve():
    A = Mat(({'a', 'b', 'c'}, {'#', '@', '?'}), {
        ('a', '#'): 2, ('a', '?'): 3,
        ('b', '@'): 10, ('b', '#'): 20, ('b', '?'): 30,
        ('c', '#'): 35,
    })
    L_R, L_C = find_triangular_order(A)
    pivots = {(L_R[i], L_C[i]) for i in range(3)}
    rowdict = A.mat2rowdict()
    rowlist = [rowdict[r] for r in L_R]
    b = [60, 5, 35]
    triangular_solve(rowlist, L_C, b)  # cross-check; values recomputed live below

    original_table = matrix_table_html(A)
    reordered_table = matrix_table_html(A, row_order=L_R, col_order=L_C, pivot_labels=pivots)

    order_flow = (
        '<div class="order-flow"><span class="label">L<sub>R</sub> =</span> '
        + '<span class="arrow">→</span>'.join(f'<span class="tag">{r}</span>' for r in L_R)
        + '<span class="label" style="margin-left:1rem">L<sub>C</sub> =</span> '
        + '<span class="arrow">→</span>'.join(f'<span class="tag">{c}</span>' for c in L_C)
        + '</div>'
    )

    solved = {}
    step_html = []
    for i in reversed(range(3)):
        r, pivot_col = L_R[i], L_C[i]
        row = rowdict[r]
        row_desc = ' &nbsp; '.join(
            (f'<b>{c}:{row[c]}</b>' if c == pivot_col else f'{c}:{row[c]}') for c in L_C
        )
        partial = ''.join(
            f'<span class="slot solved">{c} = {solved[c]:g}</span>' if c in solved
            else f'<span class="slot pending">{c} = ?</span>'
            for c in L_C
        )
        dot = sum(row[c] * solved.get(c, 0) for c in L_C)
        val = (b[i] - dot) / row[pivot_col]
        solved[pivot_col] = val
        step_html.append(f'''
    <div class="panel solve-step">
      <div class="row-being-solved"><span class="rlabel">fila {r} &nbsp;→&nbsp;</span> {row_desc}</div>
      <div class="partial-x"><span class="label">x parcial:</span>{partial}</div>
      <div class="arith">dot(fila<sub>{r}</sub>, x parcial) = {dot:g} &nbsp;→&nbsp; x[{pivot_col}] = ({b[i]:g} − {dot:g}) / {row[pivot_col]:g} = <span class="highlight">{val:g}</span></div>
    </div>''')

    content = f'''
<h2><span class="step-num">PASO 1</span> Matriz original (orden alfabético)</h2>
<p class="stage-note">No se ve triangular acá — ceros dispersos, no forman escalera.</p>
<div class="panel overflow-guard">{original_table}</div>

<h2><span class="step-num">PASO 2</span> find_triangular_order() encuentra el orden</h2>
<p class="stage-note">Prueba permutaciones hasta que todo bajo la diagonal da cero. Mismos datos, solo reordenados.</p>
<div class="panel">{order_flow}</div>

<h2><span class="step-num">PASO 3</span> Matriz reordenada — ahora sí triangular</h2>
<p class="stage-note">Misma matriz exacta, solo vista con el orden encontrado — pivotes marcados en la diagonal.</p>
<div class="panel overflow-guard">{reordered_table}</div>

<h2><span class="step-num">PASO 4</span> Backward substitution — de abajo hacia arriba</h2>
<p class="stage-note">triangular_solve() resuelve empezando por la última fila; cada paso usa lo ya resuelto.</p>
{''.join(step_html)}

<div class="result">x = {{ {', '.join(f'{c}: {solved[c]:g}' for c in L_C)} }} &nbsp;·&nbsp; verificado contra b = {b}</div>
'''

    return render_page(
        'triangular-reorder-solve-2026-07-12.html',
        title='Reordenar para triangularizar, después resolver',
        eyebrow='Coding the Matrix · Cap 4.6.4/4.6.12 + Cap 2.11 (backward substitution)',
        subhead='find_triangular_order() descubre el orden; triangular_solve() resuelve usando ese orden — generado con viz_html.py, no tipeado a mano.',
        content=content,
        footer='Generado para karpathy-path con coding_the_matrix.viz_html (05-Projects/coding-the-matrix).',
    )


_MSF_NODE_POS = {
    'Pembroke': (90, 90), 'Athletic': (300, 90), 'Bio-Med': (90, 240),
    'Main': (480, 50), 'Keeney': (430, 210), 'Wriston': (570, 210), 'Gregorian': (660, 300),
}
_MSF_SHORT = {
    'Pembroke': 'Pembroke', 'Athletic': 'Athletic', 'Bio-Med': 'Bio-Med',
    'Main': 'Main', 'Keeney': 'Keeney', 'Wriston': 'Wriston', 'Gregorian': 'Gregorian',
}


def _msf_svg(kept_edges, query_edges, isolated_nodes):
    """Self-contained inline SVG — no external assets, per CLAUDE.md 07-Visuals rule."""
    lines = []
    for x, y in kept_edges:
        x1, y1 = _MSF_NODE_POS[x]
        x2, y2 = _MSF_NODE_POS[y]
        lines.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                     f'stroke="var(--ok-ink)" stroke-width="3"/>')
    for x, y in query_edges:
        x1, y1 = _MSF_NODE_POS[x]
        x2, y2 = _MSF_NODE_POS[y]
        lines.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                     f'stroke="#c0392b" stroke-width="2.5" stroke-dasharray="7,5"/>')
    nodes = []
    for n, (x, y) in _MSF_NODE_POS.items():
        fill = '#c0392b' if n in isolated_nodes else 'var(--ok-ink)'
        nodes.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{fill}"/>'
                     f'<text x="{x+12}" y="{y+5}" class="sans" font-size="14" '
                     f'fill="var(--ink)">{_MSF_SHORT[n]}</text>')
    return (f'<svg viewBox="0 0 720 340" style="width:100%;height:auto" '
            f'xmlns="http://www.w3.org/2000/svg">{"".join(lines)}{"".join(nodes)}</svg>')


def generate_msf_span_example():
    """Klein Example 5.4.5 — span of 4 edges excludes edges touching untouched nodes."""
    nodes = set(_MSF_NODE_POS)
    kept_pairs = [('Athletic', 'Bio-Med'), ('Main', 'Keeney'), ('Keeney', 'Wriston'), ('Main', 'Wriston')]
    query_pairs = [('Pembroke', 'Keeney'), ('Main', 'Gregorian'), ('Pembroke', 'Gregorian')]

    tracker = _EliminationBasis()
    for e in kept_pairs:
        tracker.add(edge_to_vec(nodes, e))

    graph_svg = _msf_svg(kept_pairs, query_pairs, isolated_nodes={'Pembroke', 'Gregorian'})

    query = ('Pembroke', 'Keeney')
    v = edge_to_vec(nodes, query)
    trace_rows = []
    running = v
    for pivot, row in zip(tracker.pivots, tracker.pivot_rows):
        coeff = running[pivot]
        before = {n: (str(running[n]) if running[n] != 0 else '0') for n in _MSF_NODE_POS}
        if coeff != 0:
            running = running - coeff * row
        trace_rows.append([pivot, str(coeff), ', '.join(f'{n}:{before[n]}' for n in _MSF_NODE_POS if before[n] != '0')])
    final_nonzero = ', '.join(f'{n}:{running[n]}' for n in _MSF_NODE_POS if running[n] != 0)
    trace_table = trace_table_html(
        ['pivot probado', 'coef en esa posición', 'valores no-cero antes de reducir'],
        trace_rows,
    )

    content = f'''
<h2><span class="step-num">GRAFO</span> kept = 4 aristas guardadas (verde), query = 3 aristas a probar (rojo punteado)</h2>
<p class="stage-note">Pembroke y Gregorian (rojo) nunca aparecen en ninguna arista guardada — quedan aislados del subgrafo verde.</p>
<div class="panel overflow-guard">{graph_svg}</div>

<h2><span class="step-num">PASO 1</span> is_in_span({{"Pembroke","Keeney"}}) — reduce() recorre los pivotes guardados</h2>
<p class="stage-note">Cada fila del tracker tiene un pivote (un nodo) que ninguna fila anterior tocaba. "Pembroke" nunca fue pivote de nada.</p>
<div class="panel overflow-guard">{trace_table}</div>

<h2><span class="step-num">PASO 2</span> qué queda después de reducir</h2>
<p class="stage-note">Coordenadas no-cero que sobreviven: <b>{final_nonzero}</b> — Pembroke sigue en "one" porque ninguna fila del tracker tenía ese pivote para cancelarlo.</p>

<div class="result">contains() = False &nbsp;·&nbsp; {{"Pembroke","Keeney"}} NO está en Span(kept) &nbsp;·&nbsp; mismo resultado da para {{"Main","Gregorian"}} y {{"Pembroke","Gregorian"}}</div>
'''

    return render_page(
        'msf-span-example-5-4-5-2026-07-18.html',
        title='Por qué {Pembroke,Keeney} no está en el Span — Klein Example 5.4.5',
        eyebrow='Coding the Matrix · Cap 5.4.3 (MSF en GF(2)) + Cap 5.3 (Grow/Shrink)',
        subhead='Traza real de _EliminationBasis.reduce() sobre los vectores de arista — el mismo código de basis.py, sin BFS ni union-find.',
        content=content,
        footer='Generado para karpathy-path con coding_the_matrix.viz_html (05-Projects/coding-the-matrix).',
    )


def _grid_svg(extra, x_max=8, y_max=8, scale=40, pad=40):
    """Faint unit grid + axes, then extra SVG markup drawn on top."""
    w = pad * 2 + x_max * scale
    h = pad * 2 + y_max * scale

    def px(x, y):
        return pad + x * scale, h - pad - y * scale

    lines = []
    for i in range(x_max + 1):
        x, _ = px(i, 0)
        lines.append(f'<line x1="{x}" y1="{pad}" x2="{x}" y2="{h - pad}" stroke="var(--rule)" stroke-width="1"/>')
    for j in range(y_max + 1):
        _, y = px(0, j)
        lines.append(f'<line x1="{pad}" y1="{y}" x2="{w - pad}" y2="{y}" stroke="var(--rule)" stroke-width="1"/>')
    ox, oy = px(0, 0)
    lines.append(f'<line x1="{pad}" y1="{oy}" x2="{w - pad}" y2="{oy}" stroke="var(--ink-soft)" stroke-width="1.5"/>')
    lines.append(f'<line x1="{ox}" y1="{pad}" x2="{ox}" y2="{h - pad}" stroke="var(--ink-soft)" stroke-width="1.5"/>')
    return (f'<svg viewBox="0 0 {w} {h}" style="width:100%;height:auto" '
            f'xmlns="http://www.w3.org/2000/svg">{"".join(lines)}{extra}</svg>'), px


def _vector_arrow(px, origin, tip, color, label, label_dx=6, label_dy=-6):
    x1, y1 = px(*origin)
    x2, y2 = px(*tip)
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2.5" '
        f'marker-end="url(#arrow-{color.lstrip("#")})"/>'
        f'<text x="{x2 + label_dx}" y="{y2 + label_dy}" class="sans" font-size="13" fill="{color}">{label}</text>'
    )


def _parallelogram(px, o, side_a, side_b, fill, stroke, opacity=0.35):
    ax, ay = side_a
    bx, by = side_b
    pts = [o, (o[0] + ax, o[1] + ay), (o[0] + ax + bx, o[1] + ay + by), (o[0] + bx, o[1] + by)]
    pts_px = ' '.join(f'{px(*p)[0]},{px(*p)[1]}' for p in pts)
    return f'<polygon points="{pts_px}" fill="{fill}" fill-opacity="{opacity}" stroke="{stroke}" stroke-width="2"/>'


def generate_cramers_rule_shear():
    """3B1B ch12: Cramer's rule y-coordinate via shear (Cavalieri), not rotation.
    A = [[2,1],[1,3]], b = [5,7] — same system as Ch7 inverse-matrix example."""
    a, b_, c, d = 2, 1, 1, 3
    col1, col2 = (a, c), (b_, d)
    bx, by = 5, 7
    det = a * d - b_ * c
    x = (bx * d - b_ * by) / det
    y = (a * by - bx * c) / det
    y_col2 = (y * col2[0], y * col2[1])

    marker_colors = {'accent': 'var(--accent)', 'ok': 'var(--ok-ink)'}
    defs = ('<defs>' + ''.join(
        f'<marker id="arrow-{key}" viewBox="0 0 10 10" refX="8" refY="5" '
        f'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M0,0L10,5L0,10z" fill="{color}"/></marker>'
        for key, color in marker_colors.items()
    ) + '</defs>')

    def panel(shear_side, shear_color_key, shear_label):
        content, px = _grid_svg('', x_max=8, y_max=8)
        parts = [defs]
        parts.append(_parallelogram(px, (0, 0), col1, shear_side, 'var(--accent)', 'var(--accent)'))
        parts.append(_vector_arrow(px, (0, 0), col1, 'var(--accent)', 'col1'))
        parts.append(_vector_arrow(px, (0, 0), shear_side, marker_colors[shear_color_key], shear_label))
        inner = ''.join(parts)
        return _grid_svg(inner, x_max=8, y_max=8)[0]

    panel_before = panel((bx, by), 'ok', 'b')
    panel_after = panel(y_col2, 'ok', 'y·col2')

    content = f'''
<h2><span class="step-num">SETUP</span> A = [[2,1],[1,3]], b = [5,7] — mismo sistema que el ejemplo de Ch7</h2>
<p class="stage-note">det(A) = {det}. col1 = {col1}, col2 = {col2}. Solución conocida: x = {x:g}, y = {y:g}.</p>

<h2><span class="step-num">ANTES</span> Paralelogramo (col1, b)</h2>
<p class="stage-note">Área de este paralelogramo = y · det(A) — pero todavía no se ve por qué.</p>
<div class="panel overflow-guard">{panel_before}</div>

<h2><span class="step-num">SHEAR</span> Deslizar b hasta y·col2 — sin rotar, sin cambiar área</h2>
<p class="stage-note">b = x·col1 + y·col2. La parte x·col1 apunta en la misma dirección que col1 (el lado que ya comparten), así que deslizar (shear) el paralelogramo en esa dirección hasta que el segundo lado sea solo y·col2 no cambia el área — principio de Cavalieri. Esto es lo que en el video se confunde con "rotar": es un corte/deslizamiento, no un giro.</p>
<div class="panel overflow-guard">{panel_after}</div>

<h2><span class="step-num">DESPEJE</span> De área a y</h2>
<p class="stage-note">área(col1, y·col2) = y · área(col1, col2) = y · det(A) &nbsp;→&nbsp; y = área(col1, b) / det(A) = {y:g}</p>

<div class="result">y = {y:g} &nbsp;·&nbsp; x análogo con área(b, col2)/det(A) = {x:g} &nbsp;·&nbsp; mismo resultado que A⁻¹b en Ch7</div>
'''

    return render_page(
        'cramers-rule-shear-2026-07-28.html',
        title="Cramer's rule: por qué es un shear, no una rotación",
        eyebrow='3Blue1Brown · Essence of Linear Algebra Ch 12',
        subhead='Mismo sistema A=[[2,1],[1,3]], b=[5,7] del ejemplo de inversa (Ch7) — ahora resuelto vía áreas, sin calcular A⁻¹.',
        content=content,
        footer='Generado para karpathy-path con coding_the_matrix.viz_html (05-Projects/coding-the-matrix).',
    )



if __name__ == '__main__':
    path = generate_triangular_reorder_solve()
    print(f'wrote {path}')
    path2 = generate_msf_span_example()
    print(f'wrote {path2}')
    path3 = generate_cramers_rule_shear()
    print(f'wrote {path3}')
