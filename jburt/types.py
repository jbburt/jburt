import pathlib
from typing import Generic
from typing import TypeVar

import numpy as np

PathLike = TypeVar("PathLike", str, pathlib.Path)
Numeric = TypeVar("Numeric", int, float, complex, np.number)

# // Begin src = https://stackoverflow.com/a/64032593
Shape = TypeVar("Shape")
DType = TypeVar("DType")


class Array(np.ndarray, Generic[Shape, DType]):
    """
    Use this to type-annotate numpy arrays, e.g.
        image: Array['H,W,3', np.uint8]
        xy_points: Array['N,2', float]
        nd_mask: Array['...', bool]
    """

    pass


# // End
