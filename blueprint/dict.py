"""Dict module."""


class Dict(dict):
    """Dict class where keys can be accessed as attributes."""

    __slots__ = ()
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
