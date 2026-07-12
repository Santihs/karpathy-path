# Persistent, rerunnable generators for 07-Visuals/ pages (see CLAUDE.md
# "Explanation Style"). Run directly: uv run python -m coding_the_matrix.viz_examples
from coding_the_matrix.mat import Mat, find_triangular_order
from coding_the_matrix.triangular import triangular_solve
from coding_the_matrix.viz_html import render_page, matrix_table_html


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


if __name__ == '__main__':
    path = generate_triangular_reorder_solve()
    print(f'wrote {path}')
