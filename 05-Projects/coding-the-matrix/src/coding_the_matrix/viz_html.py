# Generates local, self-contained HTML explanations into vault-root/07-Visuals/,
# using one shared Jinja2 template (07-Visuals/_template.html) instead of
# hand-typing a full HTML+CSS document per example. See CLAUDE.md "Explanation
# Style": these exist because the chat surface can't render LaTeX/subscripts/ANSI.
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

_VISUALS_DIR = Path(__file__).resolve().parents[4] / "07-Visuals"


def render_page(out_name, title, eyebrow, subhead, content, footer=""):
    """
    Renders content (a string of HTML fragments) into the shared template and
    writes it to 07-Visuals/<out_name>. Returns the written path.
    """
    env = Environment(loader=FileSystemLoader(str(_VISUALS_DIR)), autoescape=False)
    html = env.get_template("_template.html").render(
        title=title, eyebrow=eyebrow, subhead=subhead, content=content, footer=footer)
    out_path = _VISUALS_DIR / out_name
    out_path.write_text(html)
    return out_path


def matrix_table_html(M, row_order=None, col_order=None, highlight_row=None, pivot_labels=None):
    """
    Renders a Mat as a <table class="mat"> — pulls values straight from M,
    no hand-copied numbers. row_order/col_order let you show it reordered
    (Klein 4.6.10/4.6.11); pivot_labels marks (row,col) pairs as diagonal
    pivots (e.g. after find_triangular_order).
    """
    rows = row_order or sorted(M.D[0], key=str)
    cols = col_order or sorted(M.D[1], key=str)
    pivot_labels = pivot_labels or set()

    head = "<tr><th></th>" + "".join(f"<th>{c}</th>" for c in cols) + "</tr>"
    body = []
    for r in rows:
        row_class = ' class="active-row"' if r == highlight_row else ""
        cells = []
        for c in cols:
            v = M[r, c]
            cell_class = "zero" if v == 0 else ("pivot" if (r, c) in pivot_labels else "")
            cls_attr = f' class="{cell_class}"' if cell_class else ""
            cells.append(f"<td{cls_attr}>{v}</td>")
        body.append(f"<tr{row_class}><td>{r}</td>{''.join(cells)}</tr>")

    return f'<table class="mat">{head}{"".join(body)}</table>'


def trace_table_html(headers, rows, active_index=None):
    """
    Renders a step-trace table (e.g. cross-product component breakdown):
    headers is a list of column names, rows is a list of row-cell-lists,
    active_index (if given) bolds/highlights that row.
    """
    head = "<tr>" + "".join(f"<th>{h}</th>" for h in headers) + "</tr>"
    body = []
    for i, row in enumerate(rows):
        row_class = ' class="active"' if i == active_index else ""
        cells = "".join(f"<td>{v}</td>" for v in row)
        body.append(f"<tr{row_class}>{cells}</tr>")
    return f'<table class="trace">{head}{"".join(body)}</table>'
