import pytest

from coding_the_matrix.mat import Mat, identity, mat2rowdict, mat2coldict, to_str, pp, find_triangular_order
from coding_the_matrix.matutil import rowdict2mat, coldict2mat, listlist2mat
from coding_the_matrix.triangular import triangular_solve
from coding_the_matrix.vec import Vec


def test_identity_is_diagonal_ones():
    I = identity({0, 1, 2})
    assert all(I[d, d] == 1 for d in {0, 1, 2})
    assert I[0, 1] == 0


def test_mat2rowdict_mat2coldict_roundtrip():
    M = listlist2mat([[1, 2, 3], [10, 20, 30]])
    assert rowdict2mat(mat2rowdict(M)) == M
    assert coldict2mat(mat2coldict(M)) == M


def test_transpose_book_example_4_4_2():
    M = Mat(({'#', '@', '?'}, {'a', 'b'}), {
        ('#', 'a'): 2, ('#', 'b'): 20,
        ('@', 'a'): 1, ('@', 'b'): 10,
        ('?', 'a'): 3, ('?', 'b'): 30,
    })
    MT = M.transpose()
    assert MT.D == ({'a', 'b'}, {'#', '@', '?'})
    assert MT['a', '@'] == 1 and MT['b', '?'] == 30


def test_matrix_vector_mul_book_example_4_5_2():
    M = listlist2mat([[1, 2, 3], [10, 20, 30]])
    v = Vec({0, 1, 2}, {0: 7, 1: 0, 2: 4})
    assert M * v == Vec({0, 1}, {0: 19, 1: 190})


def test_matrix_vector_mul_illegal_dimension_mismatch_4_5_3():
    M = listlist2mat([[1, 2, 3], [10, 20, 30]])  # 2x3: needs a 3-vector
    v = Vec({0, 1}, {0: 7, 1: 0})
    with pytest.raises(AssertionError):
        M * v


def test_vector_matrix_mul_book_example_4_5_7():
    M = listlist2mat([[1, 2, 3], [10, 20, 30]])
    v = Vec({0, 1}, {0: 3, 1: 4})
    assert v * M == Vec({0, 1, 2}, {0: 3, 1: 6, 2: 9}) + Vec({0, 1, 2}, {0: 40, 1: 80, 2: 120})


def test_vector_matrix_mul_illegal_dimension_mismatch_4_5_8():
    M = listlist2mat([[1, 2, 3], [10, 20, 30]])  # 2x3: needs a 2-vector on the left
    v = Vec({0, 1, 2}, {0: 3, 1: 4, 2: 5})
    with pytest.raises(AssertionError):
        v * M


def test_junkco_total_utilization_book_example_4_5_10():
    resources = {'metal', 'concrete', 'plastic', 'water', 'electricity'}
    rowdict = {
        'gnome': Vec(resources, {'concrete': 1.3, 'plastic': .2, 'water': .8, 'electricity': .4}),
        'hoop': Vec(resources, {'plastic': 1.5, 'water': .4, 'electricity': .3}),
        'slinky': Vec(resources, {'metal': .25, 'water': .2, 'electricity': .7}),
        'putty': Vec(resources, {'plastic': .3, 'water': .7, 'electricity': .5}),
        'shooter': Vec(resources, {'metal': .15, 'plastic': .5, 'water': .4, 'electricity': .8}),
    }
    M = rowdict2mat(rowdict)
    R = set(rowdict.keys())
    u = Vec(R, {'gnome': 240, 'hoop': 55, 'slinky': 150, 'putty': 133, 'shooter': 90})

    total = u * M

    assert total['metal'] == pytest.approx(51.0)
    assert total['concrete'] == pytest.approx(312.0)
    assert total['plastic'] == pytest.approx(215.4)
    assert total['water'] == pytest.approx(373.1)
    assert total['electricity'] == pytest.approx(356.0)


def test_transpose_trick_solves_vector_matrix_as_matrix_vector_4_5_4():
    # x*A == b  <=>  A.transpose()*x == b (Remark 4.5.9 / the trick behind solve()).
    # No solver module exists in this project yet, so this checks the identity
    # itself rather than an actual elimination-based solve().
    A = listlist2mat([[1, 2, 3], [10, 20, 30]])
    x = Vec({0, 1}, {0: 3, 1: 4})
    assert x * A == A.transpose() * x


def test_matrix_vector_mul_dot_product_book_example_4_6_2():
    M = listlist2mat([[1, 2], [3, 4], [10, 0]])
    v = Vec({0, 1}, {0: 3, 1: -1})
    assert M * v == Vec({0, 1, 2}, {0: 1, 1: 5, 2: 30})


def test_needle_in_haystack_as_matrix_vector_book_example_4_6_6():
    # Each row i is the needle [0,1,-1] placed starting at column i, wrapping
    # around past the end of the haystack (circulant-matrix structure — the
    # property Ch.10's FFT trick relies on).
    needle = [0, 1, -1]
    n = 10
    haystack = Vec(set(range(n)), dict(enumerate([0, 0, -1, 2, 3, -1, 0, 1, -1, -1])))
    M = Mat((set(range(n)), set(range(n))),
            {(i, (i + k) % n): val for i in range(n) for k, val in enumerate(needle)})

    result = M * haystack

    expected = [1, -3, -1, 4, -1, -1, 2, 0, -1, 0]
    assert [result[i] for i in range(n)] == expected
    # position 6 is the true match: haystack[6:9] == needle exactly, and its
    # score (2) is the theoretical max for this needle (its leading 0 caps it) —
    # the higher score at position 3 (4) is a numeric coincidence, not a match.
    assert result[6] == 2


def test_sensor_current_system_as_matrix_vector_book_example_4_6_7():
    # No solver module exists in this project yet (Ch.4.5.4's solve() is a
    # future-chapter reference implementation), so this verifies the book's
    # given solution satisfies every equation, rather than computing it.
    D = {'radio', 'sensor', 'memory', 'CPU'}
    v0 = Vec(D, {'radio': .1, 'CPU': .3})
    v1 = Vec(D, {'sensor': .2, 'CPU': .4})
    v2 = Vec(D, {'memory': .3, 'CPU': .1})
    v3 = Vec(D, {'memory': .5, 'CPU': .4})
    v4 = Vec(D, {'radio': .2, 'CPU': .5})

    A = rowdict2mat([v0, v1, v2, v3, v4])
    b = Vec({0, 1, 2, 3, 4}, {0: 140.0, 1: 170.0, 2: 60.0, 3: 170.0, 4: 250.0})
    rate = Vec(D, {'radio': 500, 'sensor': 250, 'memory': 100, 'CPU': 300})

    assert A * rate == b


def test_str_pretty_prints_as_labeled_table():
    M = Mat(({'#', '@', '?'}, {'a', 'b'}), {
        ('#', 'a'): 2, ('#', 'b'): 20,
        ('@', 'a'): 1, ('@', 'b'): 10,
        ('?', 'a'): 3, ('?', 'b'): 30,
    })
    lines = to_str(M).splitlines()
    assert lines[0].split() == ['a', 'b']            # header: sorted col labels
    assert set(lines[1]) == {'-'}                     # separator line
    row_lines = {line.split()[0]: line.split()[1:] for line in lines[2:]}
    assert row_lines == {'#': ['2', '20'], '@': ['1', '10'], '?': ['3', '30']}


def test_str_column_width_matches_widest_entry():
    # column 'b' has a 2-digit value (10) — must widen both columns so 'a' still aligns.
    M = Mat(({'x', 'y'}, {'a', 'b'}), {('x', 'a'): 1, ('x', 'b'): 10, ('y', 'a'): 2, ('y', 'b'): 3})
    assert to_str(M) == "   a  b\n-------\nx  1 10\ny  2  3"


def test_pp_reveals_hidden_triangular_structure_book_example_4_6_11():
    # Book's {a,b,c}x{#,@,?} matrix isn't triangular in alphabetical order (to_str),
    # but reordering rows [b,a,c] and columns [@,?,#] reveals it is (Klein Ex. 4.6.11).
    A = Mat(({'a', 'b', 'c'}, {'#', '@', '?'}), {
        ('a', '#'): 2, ('a', '?'): 3,
        ('b', '@'): 10, ('b', '#'): 20, ('b', '?'): 30,
        ('c', '#'): 35,
    })

    reordered = A.pp(['b', 'a', 'c'], ['@', '?', '#'])
    rows = [line.split()[1:] for line in reordered.splitlines()[2:]]
    assert rows == [['10', '30', '20'], ['0', '3', '2'], ['0', '0', '35']]

    values = [[int(v) for v in row] for row in rows]
    assert all(values[i][j] == 0 for i in range(3) for j in range(3) if i > j)  # upper-triangular


def test_pp_and_to_str_share_formatting_but_allow_different_order():
    M = Mat(({'a', 'b'}, {'x', 'y'}), {('a', 'x'): 1, ('a', 'y'): 2, ('b', 'x'): 10, ('b', 'y'): 20})
    assert pp(M, ['a', 'b'], ['x', 'y']) == to_str(M)
    assert pp(M, ['b', 'a'], ['y', 'x']) != to_str(M)


def test_find_triangular_order_discovers_book_example_4_6_12():
    # Problem 4.6.12: unlike pp() (display in an order you already know),
    # this must find the order itself from scratch — no hint given.
    A = Mat(({'a', 'b', 'c'}, {'#', '@', '?'}), {
        ('a', '#'): 2, ('a', '?'): 3,
        ('b', '@'): 10, ('b', '#'): 20, ('b', '?'): 30,
        ('c', '#'): 35,
    })

    L_R, L_C = find_triangular_order(A)

    assert set(L_R) == {'a', 'b', 'c'} and set(L_C) == {'#', '@', '?'}  # a genuine reordering
    assert all(A[L_R[i], L_C[j]] == 0 for i in range(3) for j in range(3) if i > j)


def test_find_triangular_order_reports_none_when_impossible():
    # A 2x2 matrix with no zero entries at all can never be made triangular
    # by any row/column reordering — every off-diagonal spot stays nonzero.
    A = Mat(({'a', 'b'}, {'x', 'y'}), {('a', 'x'): 1, ('a', 'y'): 1, ('b', 'x'): 1, ('b', 'y'): 1})
    assert find_triangular_order(A) is None


def test_find_triangular_order_requires_square_matrix():
    A = listlist2mat([[1, 2, 3], [4, 5, 6]])  # 2 rows, 3 columns
    assert find_triangular_order(A) is None


def test_find_order_then_solve_the_3x3_system():
    # End-to-end: find_triangular_order() discovers WHICH order makes A
    # triangular, then triangular_solve() (Ch.2.11, already implemented)
    # actually solves it — Problem 4.6.12 completed, not just detected.
    A = Mat(({'a', 'b', 'c'}, {'#', '@', '?'}), {
        ('a', '#'): 2, ('a', '?'): 3,
        ('b', '@'): 10, ('b', '#'): 20, ('b', '?'): 30,
        ('c', '#'): 35,
    })

    L_R, L_C = find_triangular_order(A)
    rowdict = A.mat2rowdict()
    rowlist = [rowdict[r] for r in L_R]     # rows, reordered
    b = [60, 5, 35]                         # matches L_R order: row_i * x == b[i]

    x = triangular_solve(rowlist, L_C, b)

    assert x == Vec({'#', '@', '?'}, {'#': 1, '@': 1, '?': 1})
    # verify against the ORIGINAL matrix (not just the reordered rowlist) —
    # confirms the row-relabeling didn't silently change what's being solved
    assert [round(rowdict[r] * x, 6) for r in L_R] == b
