"""
Functions that operate on matrices.
"""

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import reverse_cuthill_mckee


def reorder_rcm(mat: np.ndarray, thresh: float) -> np.ndarray:
    """
    Compute permutation of matrix rows/cols that yields block-diagonal structure
    per the reverse Cuthill-McKee algorithm.\

    Parameters
    ----------
    mat : (N,N) np.ndarray
        matrix
    thresh : float
        threshold to sparsify the graph

    Returns
    -------
    (N,) np.ndarray[int]
        reordering indices

    """

    sparsemat = csr_matrix(mat > thresh)
    return reverse_cuthill_mckee(sparsemat)


def find_diagonal_blocks(mat: np.ndarray) -> np.ndarray:
    """
    Find perfect diagonal sub-blocks in a block-diagonalized binary matrix.

    Parameters
    ----------
    mat : (n,n) np.ndarray
        binary matrix

    Returns
    -------
    inds : (n,) np.ndarray[int]
        all elements comprising a unique perfect diagonal sub-block are assigned
        the same non-zero identifier. elements not in a block are zero.

    """
    n, m = mat.shape
    assert n == m  # square
    assert np.allclose(mat, mat.T)  # symmetric
    assert set(np.unique(mat)).issubset({0, 1})  # binary
    inds = np.zeros(n)
    uid = 1
    i = 0
    while i < (n-1):
        j = i + 2
        while j <= n:
            # get current subblock
            block = mat[i:j, :][:, i:j]
            if block.all():
                j += 1
            else:
                j -= 1
                break
        if (j - 1) > i:  # found nontrivial block
            inds[i:j] = uid
            uid += 1
        i = j
    return inds.astype(int)
