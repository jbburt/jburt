import glob
import pathlib
from pathlib import Path
from typing import List
from typing import Union

from .checks import is_string_like


def strip_ext(filepath: Union[str, pathlib.Path]) -> Union[str, pathlib.Path]:
    """
    Strip extension from a file.

    Parameters
    ----------
    filepath : str or pathlib.Path

    Returns
    -------
    str or pathlib.PosixPath
        `filepath` with suffix removed. type is equivalent to input.

    """
    result = Path(filepath).with_suffix('')
    return result if isinstance(filepath, Path) else str(result)


def check_exists(filepath: Union[str, pathlib.Path]) -> bool:
    """
    Check that file exists and has nonzero size.

    Parameters
    ----------
    filepath : str or pathlib.Path

    Returns
    -------
    bool
        True if `filepath` exists and has non-zero size

    """
    if (Path(filepath).stat().st_size == 0) or (not Path(filepath).exists()):
        return False
    return True


def count_lines(file: Union[str, pathlib.Path]) -> int:
    """
    Count number of lines in a file.

    Parameters
    ----------
    file : str or pathlib.Path

    Returns
    -------
    int
        number of lines in file

    """
    with open(file, 'rb') as f:
        lines = 0
        buf_size = 1024 * 1024
        read_f = f.raw.read
        buf = read_f(buf_size)
        while buf:
            lines += buf.count(b'\n')
            buf = read_f(buf_size)
        return lines


def child_files_recursive(root: Union[str, pathlib.Path], ext: str) -> List[str]:
    """
    Get all files with a specific extension nested under a root directory.

    Parameters
    ----------
    root : pathlib.Path or str
        root directory
    ext : str
        file extension

    Returns
    -------
    List[str]

    """
    if not is_string_like(root) and not isinstance(root, pathlib.Path):
        raise TypeError(f'filetype is not string-like: {type(root)}')
    return list(glob.iglob(str(Path(root).joinpath('**/*' + ext)), recursive=True))
