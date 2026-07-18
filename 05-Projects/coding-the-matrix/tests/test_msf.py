from coding_the_matrix.msf import edge_to_vec, msf_grow, msf_shrink
from coding_the_matrix.basis import is_in_span

NODES = {"Pembroke", "Athletic", "Bio-Med", "Main", "Keeney", "Wriston", "Gregorian"}

# Klein Fig. 5.4 / Example 5.4.1 — Brown University hot-water network.
EDGES = [
    (7, ("Pembroke", "Athletic")),
    (2, ("Pembroke", "Bio-Med")),
    (9, ("Athletic", "Bio-Med")),
    (5, ("Main", "Keeney")),
    (3, ("Main", "Wriston")),
    (4, ("Keeney", "Wriston")),
    (8, ("Keeney", "Gregorian")),
    (6, ("Wriston", "Gregorian")),
]


def test_edge_to_vec_has_ones_only_at_endpoints():
    v = edge_to_vec(NODES, ("Main", "Keeney"))
    assert v["Main"] == 1 or str(v["Main"]) == "one"
    assert v["Wriston"] == 0


def test_msf_grow_matches_book_solution():
    chosen = msf_grow(NODES, EDGES)
    assert sorted(w for w, e in EDGES if e in chosen) == [2, 3, 4, 6, 7]


def test_msf_shrink_matches_book_solution():
    chosen = msf_shrink(NODES, EDGES)
    assert sorted(w for w, e in EDGES if e in chosen) == [2, 3, 4, 6, 7]


def test_grow_and_shrink_agree_on_total_weight():
    grow_weight = sum(w for w, e in EDGES if e in msf_grow(NODES, EDGES))
    shrink_weight = sum(w for w, e in EDGES if e in msf_shrink(NODES, EDGES))
    assert grow_weight == shrink_weight


def test_example_5_4_4_span_contains_path_edge_not_others():
    # Span of {Pem,BioMed},{Main,Wriston},{Keeney,Wriston},{Wriston,Greg}
    kept = [
        edge_to_vec(NODES, ("Pembroke", "Bio-Med")),
        edge_to_vec(NODES, ("Main", "Wriston")),
        edge_to_vec(NODES, ("Keeney", "Wriston")),
        edge_to_vec(NODES, ("Wriston", "Gregorian")),
    ]
    # path Main-Wriston-Keeney exists in `kept` -> {Main,Keeney} is reachable
    assert is_in_span(kept, edge_to_vec(NODES, ("Main", "Keeney")))
    # Athletic is untouched by `kept` -> unreachable
    assert not is_in_span(kept, edge_to_vec(NODES, ("Athletic", "Bio-Med")))
    # Bio-Med's component {Pembroke,Bio-Med} is disconnected from Main's component
    assert not is_in_span(kept, edge_to_vec(NODES, ("Bio-Med", "Main")))


def test_example_5_4_5_span_excludes_edges_touching_untouched_nodes():
    # Span of {Athletic,BioMed},{Main,Keeney},{Keeney,Wriston},{Main,Wriston}
    kept = [
        edge_to_vec(NODES, ("Athletic", "Bio-Med")),
        edge_to_vec(NODES, ("Main", "Keeney")),
        edge_to_vec(NODES, ("Keeney", "Wriston")),
        edge_to_vec(NODES, ("Main", "Wriston")),
    ]
    # Pembroke and Gregorian are never touched by `kept` -> any edge naming them is unreachable
    assert not is_in_span(kept, edge_to_vec(NODES, ("Pembroke", "Keeney")))
    assert not is_in_span(kept, edge_to_vec(NODES, ("Main", "Gregorian")))
    assert not is_in_span(kept, edge_to_vec(NODES, ("Pembroke", "Gregorian")))
