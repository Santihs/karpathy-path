# Klein, "Coding the Matrix", Ch. 5.4 — Minimum Spanning Forest via Grow/Shrink,
# formulated in linear algebra over GF(2) (Sec. 5.4.3). Each edge {x,y} becomes
# a Vec over the node domain with `one` at x and y, zero elsewhere. Summing the
# vectors of a path cancels every interior node (one+one=0 in GF(2)), leaving
# just the two endpoints — so "is edge e in Span(kept edges)" is EXACTLY
# "does e's cycle-test pass", i.e. are e's endpoints already connected by what
# Grow/Shrink kept. That's why basis.is_in_span (built for Ch. 5.3 vectors)
# works here unchanged.
from coding_the_matrix.vec import Vec
from coding_the_matrix.gf2 import one
from coding_the_matrix.basis import is_in_span


def edge_to_vec(nodes, edge):
    """
    >>> nodes = {'a', 'b', 'c'}
    >>> v = edge_to_vec(nodes, ('a', 'b'))
    >>> v['a'], v['b'], v['c']
    (one, one, 0)
    """
    x, y = edge
    return Vec(nodes, {x: one, y: one})


def msf_grow(nodes, weighted_edges):
    """
    Klein 5.4.2 Grow: consider edges lowest-weight first, keep an edge iff its
    vector is not in the span of the ones already kept (endpoints not yet
    connected). Brown University campus example (Klein Fig. 5.4/Example 5.4.1):

    >>> nodes = {'Pembroke', 'Athletic', 'Bio-Med', 'Main', 'Keeney', 'Wriston', 'Gregorian'}
    >>> edges = [
    ...     (7, ('Pembroke', 'Athletic')), (2, ('Pembroke', 'Bio-Med')),
    ...     (9, ('Athletic', 'Bio-Med')), (5, ('Main', 'Keeney')),
    ...     (3, ('Main', 'Wriston')), (4, ('Keeney', 'Wriston')),
    ...     (8, ('Keeney', 'Gregorian')), (6, ('Wriston', 'Gregorian')),
    ... ]
    >>> chosen = msf_grow(nodes, edges)
    >>> sorted(w for w, e in edges if e in chosen)
    [2, 3, 4, 6, 7]
    """
    ordered = sorted(weighted_edges, key=lambda we: we[0])
    kept_vecs, kept_edges = [], []
    for w, e in ordered:
        v = edge_to_vec(nodes, e)
        if not is_in_span(kept_vecs, v):
            kept_vecs.append(v)
            kept_edges.append(e)
    return kept_edges


def msf_shrink(nodes, weighted_edges):
    """
    Klein 5.4.2 Shrink: start with every edge, consider highest-weight first,
    drop an edge iff it's in the span of the rest (endpoints stay connected
    without it). Same campus example — Grow and Shrink land on the same
    total weight, the point Klein makes right after Example 5.3.2.

    >>> nodes = {'Pembroke', 'Athletic', 'Bio-Med', 'Main', 'Keeney', 'Wriston', 'Gregorian'}
    >>> edges = [
    ...     (7, ('Pembroke', 'Athletic')), (2, ('Pembroke', 'Bio-Med')),
    ...     (9, ('Athletic', 'Bio-Med')), (5, ('Main', 'Keeney')),
    ...     (3, ('Main', 'Wriston')), (4, ('Keeney', 'Wriston')),
    ...     (8, ('Keeney', 'Gregorian')), (6, ('Wriston', 'Gregorian')),
    ... ]
    >>> chosen = msf_shrink(nodes, edges)
    >>> sorted(w for w, e in edges if e in chosen)
    [2, 3, 4, 6, 7]
    """
    ordered = sorted(weighted_edges, key=lambda we: -we[0])
    B = list(weighted_edges)
    for w, e in ordered:
        rest = [(w2, e2) for w2, e2 in B if e2 != e]
        rest_vecs = [edge_to_vec(nodes, e2) for w2, e2 in rest]
        if is_in_span(rest_vecs, edge_to_vec(nodes, e)):
            B = rest
    return [e for w, e in B]
