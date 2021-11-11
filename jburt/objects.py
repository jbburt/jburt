"""
Custom object definitions.

"""


class dotdict(dict):
    """dot notation get-access to dictionary attributes"""

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError as e:
            raise AttributeError from e

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
