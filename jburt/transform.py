from typing import Generator


def flatten(nested) -> Generator:
    """
    Flatten elements in nested iterable objects.

    Parameters
    ----------
    nested : list or np.ndarray
        nested lists/arrays

    Returns
    -------
    Generator

    """
    for sublist in nested:
        if hasattr(sublist, '__iter__'):
            for element in flatten(sublist):
                yield element
        else:
            yield sublist
