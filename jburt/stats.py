from typing import Collection
from typing import Tuple

import numpy as np
from scipy import special as special
from scipy.stats import pearsonr
from scipy.stats import rankdata

from jburt.mask import mask_nan


def nonparp(stat: float, null_dist: Collection) -> float:
    """
    Compute two-sided non-parametric p-value.

    Compute the fraction of elements in `dist` which are more extreme than
    `stat`.

    Parameters
    ----------
    stat : float
        test statistic
    null_dist : Collection
        samples from null distribution

    Returns
    -------
    float
        Fraction of elements in `dist` which are more extreme than `stat`

    """
    n = float(len(null_dist))
    return np.sum(np.abs(null_dist) > abs(stat)) / n


def abs_pearson(x: np.ndarray, y: np.ndarray) -> float:
    """
    Compute absolute value of Pearson correlation coefficient.

    Parameters
    ----------
    x : (N,) np.ndarray
    y : (N,) np.ndarray

    Returns
    -------
    r : float
        absolute value of correlation

    """
    return abs(pearsonr(x, y)[0])


def pearsonr_multi(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    """
    Multi-dimensional Pearson correlation between rows of `X` and `Y`.

    Parameters
    ----------
    X : (N,P) np.ndarray
    Y : (M,P) np.ndarray

    Returns
    -------
    (N,M) np.ndarray

    Raises
    ------
    TypeError : `X` or `Y` is not array_like
    ValueError : `X` and `Y` are not same size along second axis

    """
    if not isinstance(X, np.ndarray) or not isinstance(Y, np.ndarray):
        raise TypeError('X and Y must be numpy arrays')

    if X.ndim == 1:
        X = X.reshape(1, -1)
    if Y.ndim == 1:
        Y = Y.reshape(1, -1)

    n = X.shape[1]
    if n != Y.shape[1]:
        raise ValueError('X and Y must be same size along axis=1')

    mu_x = X.mean(axis=1)
    mu_y = Y.mean(axis=1)

    s_x = X.std(axis=1, ddof=n - 1)
    s_y = Y.std(axis=1, ddof=n - 1)
    cov = np.dot(X, Y.T) - n * np.dot(
        mu_x[:, np.newaxis], mu_y[np.newaxis, :])
    return cov / np.dot(s_x[:, np.newaxis], s_y[np.newaxis, :])


def spearmanr_multi(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    """
    Multi-dimensional Spearman rank correlation between rows of `X` and `Y`.

    Parameters
    ----------
    X : (N,P) np.ndarray
    Y : (M,P) np.ndarray

    Returns
    -------
    (N,M) np.ndarray

    Raises
    ------
    TypeError : `X` or `Y` is not array_like
    ValueError : `X` and `Y` are not same size along second axis

    Notes
    -----
    Spearman rank correlation is equivalent to performing pearson correlation on
    ranks.

    """
    return pearsonr_multi(rankdata(X, axis=1), rankdata(Y, axis=1))


def pairwise_r(X: np.ndarray, flatten: bool = False) -> np.ndarray:
    """
    Compute pairwise Pearson's r between rows of `X`.

    Parameters
    ----------
    X : (N,M) np.ndarray
        N rows each with M numeric elements
    flatten : bool, default False
        If True, return flattened upper triangular elements of corr. matrix

    Returns
    -------
    (N*(N-1)/2,) or (N,N) np.ndarray
        Pearson correlation coefficients

    """
    rp = pearsonr_multi(X, X)
    if not flatten:
        return rp
    triu_inds = np.triu_indices_from(rp, k=1)
    return rp[triu_inds].flatten()


def pairwise_rho(X: np.ndarray, flatten: bool = False) -> np.ndarray:
    """
    Compute pairwise Spearman's rho between rows of `X`.

    Parameters
    ----------
    X : (N,M) np.ndarray
        N rows each with M numeric elements
    flatten : bool, default False
        If True, return flattened upper triangular elements of corr. matrix

    Returns
    -------
    (N*(N-1)/2,) or (N,N) np.ndarray
        Pearson correlation coefficients

    """
    rp = spearmanr_multi(X, X)
    if not flatten:
        return rp
    triu_inds = np.triu_indices_from(rp, k=1)
    return rp[triu_inds].flatten()


def wmean(x: np.ndarray, w: np.ndarray) -> float:
    """
    Compute weighted mean of an array.

    Parameters
    ----------
    x : (N,) np.ndarray
        scalar array
    w : (N,) np.ndarray
        weight for each element of ``x``

    Returns
    -------
    float
        weighted mean

    """
    return np.sum(w * x) / np.sum(w)


def wcov(x: np.ndarray, y: np.ndarray, w: np.ndarray) -> float:
    """
    Compute weighted covariance between two arrays.

    Parameters
    ----------
    x : (N,) np.ndarray
        scalar array
    y : (N,) np.ndarray
        scalar array
    w : (N,) np.ndarray
        weights

    Returns
    -------
    float
        weighted covariance

    """
    assert x.size == y.size
    assert x.size == w.size
    return np.sum(w * (x - wmean(x, w)) * (y - wmean(y, w))) / np.sum(w)


def wcorr(x: np.ndarray, y: np.ndarray, w: np.ndarray) -> float:
    """
    Compute weighted correlation between two arrays.

    Parameters
    ----------
    x : (N,) np.ndarray
        scalar array
    y : (N,) np.ndarray
        scalar array
    w : (N,) np.ndarray
        weights

    Returns
    -------
    float
        weighted correlation

    """
    return wcov(x, y, w) / np.sqrt(wcov(x, x, w) * wcov(y, y, w))


def p_2tailed(r: float, n: int) -> float:
    """
    Compute 2-tailed p-value.

    Parameters
    ----------
    r : float
        correlation coefficient
    n : int
        degrees of freedom (length of vector used to compute ``r``)

    Returns
    -------
    float
        two-tailed p-value

    Notes
    -----
    Code adapted from scipy.stats.pearsonr

    """
    r = max(min(r, 1.0), -1.0)
    df = n - 2
    if abs(r) == 1.0:
        prob = 0.0
    else:
        t_squared = r ** 2 * (df / ((1.0 - r) * (1.0 + r)))
        prob = special.betainc(0.5 * df, 0.5, df / (df + t_squared))
    return prob


def pearsonr_weighted(
        x: np.ndarray,
        y: np.ndarray,
        w: np.ndarray = None
) -> Tuple[float]:
    """
    Compute the weighted Pearson correlation coefficient.

    Parameters
    ----------
    x : (N,) np.ndarray
        scalar array
    y : (N,) np.ndarray
        scalar array
    w : (N,) np.ndarray
        weights

    Returns
    -------
    r : float
        weighted Pearson correlation coefficient
    p : float
        two-tailed p-value

    """
    assert type(x) == type(y) == np.ndarray
    assert x.size == y.size
    if w is None:
        x, y = mask_nan([x, y])
        return pearsonr(x, y)
    else:
        assert type(w) == np.ndarray and w.size == x.size
        x, y, w = mask_nan([x, y, w])
        n = x.size
        if np.isnan(w).all():
            return np.nan, np.nan
        r = wcorr(x, y, w)
        p = p_2tailed(r, n)
        return r, p
