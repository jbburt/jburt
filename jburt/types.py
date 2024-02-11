import pathlib
from typing import Generic
from typing import TypeVar

import numpy as np

Shape = TypeVar("Shape")
DType = TypeVar("DType")
PathLike = TypeVar("PathLike", str, pathlib.Path)
Numeric = TypeVar("Numeric", int, float, complex, np.number)


class Array(np.ndarray, Generic[Shape, DType]):
    """
    Use this to type-annotate numpy arrays, e.g.
        image: Array['H,W,3', np.uint8]
        xy_points: Array['N,2', float]
        nd_mask: Array['...', bool]

    Copied from https://stackoverflow.com/a/64032593
    """

    pass
