# Klein, "Coding the Matrix", Ch. 5.3 — Grow and Shrink algorithms for finding
# a minimal generating set (basis). Both reduce to one primitive: "is v in the
# span of what we have so far?" (Fundamental Questions 5.2.4/5.2.5). That test
# is done here by incremental elimination — reduce v against a running set of
# pivot rows, one distinct pivot coordinate per row, Vec-arithmetic generic
# over any field (works unchanged for GF(2) vectors from msf.py, since Vec's
# +/-/* dispatch to whatever field element is stored, e.g. gf2.one).
from coding_the_matrix.vec import Vec


class _EliminationBasis:
    """Tracks a reduced basis incrementally so span-membership is a linear scan."""

    def __init__(self):
        self.pivot_rows = []
        self.pivots = []

    def reduce(self, v):
        for pivot, row in zip(self.pivots, self.pivot_rows):
            coeff = v[pivot]
            if coeff != 0:
                v = v - coeff * row
        return v

    def contains(self, v):
        r = self.reduce(v)
        return all(r[k] == 0 for k in r.D)

    def add(self, v):
        """Reduce v; if it's independent of what's tracked, absorb it (return True)."""
        r = self.reduce(v)
        nz = [k for k in r.D if r[k] != 0]
        if not nz:
            return False
        pivot = nz[0]
        self.pivot_rows.append(r / r[pivot])
        self.pivots.append(pivot)
        return True


def is_in_span(vectors, v):
    """
    True iff v is a linear combination of vectors — the span test behind both
    Question 5.2.4 (uniqueness) and 5.2.5 (minimality).

    >>> from coding_the_matrix.vecutil import list2vec
    >>> a1, a2 = list2vec([1, 0]), list2vec([0, 1])
    >>> a3 = a1 + a2
    >>> is_in_span([a1, a2], a3)
    True
    >>> is_in_span([a1], a2)
    False
    """
    tracker = _EliminationBasis()
    for u in vectors:
        tracker.add(u)
    return tracker.contains(v)


def grow(vectors):
    """
    Klein 5.3.1: scan vectors in order, keep v iff it's not in Span of what's
    kept so far. Stops with a basis for Span(vectors) — same size no matter
    which vectors happened to be redundant (Exchange Lemma, Klein 5.5).

    >>> from coding_the_matrix.vecutil import list2vec
    >>> e1, e2, e3 = list2vec([1,0,0]), list2vec([0,1,0]), list2vec([0,0,1])
    >>> len(grow([e1, e2, e3]))
    3
    >>> len(grow([e1, e2, e1 + e2]))
    2
    """
    tracker = _EliminationBasis()
    return [v for v in vectors if tracker.add(v)]


def shrink(vectors):
    """
    Klein 5.3.2: start from vectors (possibly redundant) and drop any vector
    that's in the span of the rest, until none can be dropped. Result spans
    the same space as the input, with no redundant vector left.

    >>> from coding_the_matrix.vecutil import list2vec
    >>> v1, v2 = list2vec([1,0,0]), list2vec([0,1,0])
    >>> v3, v4 = v1 + 2*v2, 3*v1 + v2
    >>> B = shrink([v1, v2, v3, v4])
    >>> len(B)
    2
    >>> is_in_span(B, v3) and is_in_span(B, v4)
    True
    """
    B = list(vectors)
    i = 0
    while i < len(B):
        rest = B[:i] + B[i + 1:]
        if is_in_span(rest, B[i]):
            B = rest
        else:
            i += 1
    return B
