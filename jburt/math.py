"""
General mathematical transformations and statistical methods.

"""

import numpy as np
from scipy.stats import zscore


def modified_zscore(x: np.ndarray) -> np.ndarray:
    """
    Modified z-score transformation.

    The modified z score might be more robust than the standard z-score because
    it relies on the median for calculating the z-score. It is less influenced
    by outliers when compared to the standard z-score.

    Parameters
    ----------
    x: (N,) np.ndarray
        numbers

    Returns
    -------
    z: (N,) np.ndarray
        z-scored numbers computed using modified z-score

    """
    med = np.median(x)
    med_abs_dev = np.median(np.abs(x - med))
    return (x - med) / (1.486 * med_abs_dev)


def find_outliers(scores: np.ndarray,
                  threshold: float = 3.0,
                  max_iter: int = 5,
                  tail: int = 0) -> np.ndarray:
    """
    Find outliers via iterated z-scoring.

    This procedure compares absolute z-scores against the threshold.
    After excluding outliers, the comparison is repeated until no
    outliers are present.

    Parameters
    ----------
    scores : (N,) np.ndarray
        The scores for which to find outliers.
    threshold : float, optional
        The value above which a feature is classified as outlier.
    max_iter : int, optional
        The maximum number of iterations.
    tail : one of {0, 1, -1}, optional
        Whether to search for outliers on both extremes of the z-scores (0),
        or on just the positive (1) or negative (-1) side.

    Returns
    -------
    bad_idx : (M,) np.ndarray[int]
        The indices of outliers found in `scores`.

    Notes
    -----
    This code adapted from mne.preprocessing.bads._find_outliers

    """
    bad_idx = list()
    remaining_idx = list(range(len(scores)))

    for _ in range(max_iter):
        x = scores[remaining_idx]
        if tail == 0:
            this_z = np.abs(zscore(x))
        elif tail == 1:
            this_z = zscore(x)
        elif tail == -1:
            this_z = -zscore(x)
        else:
            raise ValueError("Tail parameter %s not recognised." % tail)

        local_bad = this_z > threshold
        if not np.any(local_bad):
            break

        ix_to_remove = [remaining_idx[i] for i in np.where(local_bad)[0]]
        for ix in ix_to_remove:
            bad_idx.append(ix)
            remaining_idx.remove(ix)

    return np.array(bad_idx, dtype=int)


def rms(x: np.ndarray) -> float:
    """ Compute root-mean-square. """
    return np.sqrt(np.mean(np.power(x, 2)))


def logistic4(x: np.ndarray, a: float, b: float, c: float, d: float) -> np.ndarray:
    """
    4PL logistic equation.

    Parameters
    ----------
    x: (N,) np.ndarray
        scalar array, eg logarithmic concentration of a drug
    a: float
        response as x -> 0
    b: float
        slope
    c: float
        inflection point, eg EC50
    d: float
        response as x -> inf

    Returns
    -------
    (N,) np.ndarray
        transformation of `x`

    """
    return d + ((a - d) / (1.0 + ((-x / c) ** b)))
