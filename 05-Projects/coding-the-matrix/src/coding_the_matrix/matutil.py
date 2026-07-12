# Klein, "Coding the Matrix", Ch. 4.1.7. Conversions between Mat and rowdict/coldict/list-of-lists.
from coding_the_matrix.mat import Mat
from coding_the_matrix.vec import Vec


def rowdict2mat(rowdict):
    """
    Given a dict mapping row labels to Vecs (all sharing the same domain),
    returns the Mat with those rows. A list of Vecs is also accepted, using
    the list indices as row labels (Klein's Example 4.6.7 usage).

    >>> rowdict2mat({'a': Vec({'#','@'}, {'#':1,'@':2}), 'b': Vec({'#','@'}, {'#':10,'@':20})}) == \
        Mat(({'a','b'}, {'#','@'}), {('a','#'):1, ('a','@'):2, ('b','#'):10, ('b','@'):20})
    True
    >>> rowdict2mat([Vec({'#','@'}, {'#':1,'@':2}), Vec({'#','@'}, {'#':10,'@':20})]) == \
        Mat(({0,1}, {'#','@'}), {(0,'#'):1, (0,'@'):2, (1,'#'):10, (1,'@'):20})
    True
    """
    if isinstance(rowdict, list):
        rowdict = dict(enumerate(rowdict))
    row_labels = set(rowdict.keys())
    col_labels = next(iter(rowdict.values())).D
    return Mat((row_labels, col_labels), {(r, c): rowdict[r][c] for r in row_labels for c in col_labels})


def coldict2mat(coldict):
    """
    Given a dict mapping column labels to Vecs (all sharing the same domain),
    returns the Mat with those columns.

    >>> coldict2mat({'#': Vec({'a','b'}, {'a':1,'b':10}), '@': Vec({'a','b'}, {'a':2,'b':20})}) == \
        Mat(({'a','b'}, {'#','@'}), {('a','#'):1, ('a','@'):2, ('b','#'):10, ('b','@'):20})
    True
    """
    col_labels = set(coldict.keys())
    row_labels = next(iter(coldict.values())).D
    return Mat((row_labels, col_labels), {(r, c): coldict[c][r] for r in row_labels for c in col_labels})


def listlist2mat(L):
    """
    Given a list of lists of field elements (dense, row-major), returns the
    Mat with row/column labels {0,...,len(L)-1} / {0,...,len(L[0])-1}.

    >>> listlist2mat([[1,2,3],[10,20,30]]) == Mat(({0,1}, {0,1,2}), \
        {(0,0):1,(0,1):2,(0,2):3,(1,0):10,(1,1):20,(1,2):30})
    True
    """
    row_labels = set(range(len(L)))
    col_labels = set(range(len(L[0])))
    return Mat((row_labels, col_labels), {(r, c): L[r][c] for r in row_labels for c in col_labels})
