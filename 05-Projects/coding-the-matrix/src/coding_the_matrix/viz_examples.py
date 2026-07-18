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


if __name__ == '__main__':
    path = generate_triangular_reorder_solve()
    print(f'wrote {path}')
    path2 = generate_msf_span_example()
    print(f'wrote {path2}')
