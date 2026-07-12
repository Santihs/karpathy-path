from coding_the_matrix.mat import Mat
from coding_the_matrix.matutil import listlist2mat
from coding_the_matrix.viz_html import matrix_table_html, render_page, trace_table_html
from coding_the_matrix.viz_examples import generate_triangular_reorder_solve


def test_matrix_table_html_renders_every_cell_value():
    M = listlist2mat([[1, 2], [3, 4]])
    html = matrix_table_html(M)
    for v in [1, 2, 3, 4]:
        assert f"<td>{v}</td>" in html


def test_matrix_table_html_marks_zero_cells():
    M = Mat(({'a', 'b'}, {'x', 'y'}), {('a', 'x'): 5})  # a,y / b,x / b,y all implicit 0
    html = matrix_table_html(M)
    assert '<td class="zero">0</td>' in html
    assert '<td>5</td>' in html


def test_matrix_table_html_marks_pivot_cells():
    M = listlist2mat([[7, 0], [0, 9]])
    html = matrix_table_html(M, pivot_labels={(0, 0), (1, 1)})
    assert '<td class="pivot">7</td>' in html
    assert '<td class="pivot">9</td>' in html


def test_matrix_table_html_respects_custom_row_col_order():
    M = listlist2mat([[1, 2], [3, 4]])
    html_default = matrix_table_html(M)  # row/col order 0,1
    html_reordered = matrix_table_html(M, row_order=[1, 0], col_order=[1, 0])

    def data_rows(html):
        # row label + its 2 cell values, per <tr>, skipping the header row
        return [
            [cell.split("<")[0] for cell in row.split("<td>")[1:]]
            for row in html.split("<tr>")[2:]
        ]

    assert data_rows(html_default) == [["0", "1", "2"], ["1", "3", "4"]]
    assert data_rows(html_reordered) == [["1", "4", "3"], ["0", "2", "1"]]


def test_matrix_table_html_highlights_active_row():
    M = listlist2mat([[1, 2], [3, 4]])
    html = matrix_table_html(M, highlight_row=1)
    assert '<tr class="active-row">' in html


def test_trace_table_html_renders_headers_and_active_row():
    html = trace_table_html(
        headers=["componente", "resultado"],
        rows=[["x", -3], ["y", 6]],
        active_index=1,
    )
    assert "<th>componente</th>" in html
    assert '<tr class="active"><td>y</td><td>6</td></tr>' in html
    assert '<tr><td>x</td><td>-3</td></tr>' in html


def test_render_page_writes_file_with_content(tmp_path, monkeypatch):
    import coding_the_matrix.viz_html as viz_html
    monkeypatch.setattr(viz_html, "_VISUALS_DIR", tmp_path)
    # the shared template lives in the real 07-Visuals/, so copy it into tmp_path
    # (this test file is tests/test_viz_html.py -> parents[3] is the vault root)
    from pathlib import Path
    real_template = Path(__file__).resolve().parents[3] / "07-Visuals" / "_template.html"
    (tmp_path / "_template.html").write_text(real_template.read_text())

    out_path = viz_html.render_page(
        "demo.html", title="T", eyebrow="E", subhead="S", content="<p>hola</p>", footer="F",
    )

    assert out_path == tmp_path / "demo.html"
    written = out_path.read_text()
    assert "<title>T</title>" in written
    assert "<p>hola</p>" in written


def test_generate_triangular_reorder_solve_produces_correct_result():
    # end-to-end: the generator must reflect the real find_triangular_order +
    # triangular_solve values, not hand-copied numbers that could drift.
    out_path = generate_triangular_reorder_solve()
    html = out_path.read_text()
    assert "x = { @: 1, ?: 1, #: 1 }" in html
    assert "L<sub>R</sub>" in html and "L<sub>C</sub>" in html
