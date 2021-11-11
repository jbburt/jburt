import json
from pathlib import Path
from typing import Any
from typing import Container
from typing import Union


def is_string_like(obj: Any) -> bool:
    """ Check whether `obj` behaves like a string. """
    try:
        obj + ''
    except (TypeError, ValueError):
        return False
    return True


def is_jsonable(obj: Any) -> bool:
    """
    Check if object is jsonable.

    Parameters
    ----------
    obj : Any

    Returns
    -------
    bool

    """
    try:
        json.dumps(obj)
        return True
    except (TypeError, OverflowError):
        return False


def check_extensions(filename: Union[str, Path], exts: Container) -> bool:
    """
    Check that a filename has one of several file extensions.

    Parameters
    ----------
    filename : str or pathlib.Path
        Path to file
    exts : Container
        allowed file extensions for `filename`

    Returns
    -------
    bool
        True if `filename`'s extensions is in `exts`

    Raises
    ------
    TypeError : `filename` is not string-like
    TypeError: `exts` does not have method __contains__

    """
    if isinstance(filename, Path):
        pass
    elif not is_string_like(filename):
        raise TypeError(
            f"Expected string-like or pathlib.Path, got {type(filename)}"
        )
    if not hasattr(exts, '__contains__'):
        raise TypeError(f"object type {type(exts)} has no __contains__ method")
    ext = Path(filename).suffix
    return True if ext in exts else False
