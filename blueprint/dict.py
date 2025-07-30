"""Dict module."""


class Dict(dict):
    """Dict class where keys can be accessed as attributes."""

    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__

    def __init__(self, obj: dict = None):
        """Initialize the object."""
        if obj:
            for k, v in obj.items():
                if isinstance(v, dict):
                    obj[k] = Dict(v)
            super().__init__(obj)

    def to_dict(self):
        """Return this cast as a dict, recursively."""
        obj = dict(self)
        for k, v in obj.items():
            if isinstance(v, Dict):
                obj[k] = v.to_dict()
        return obj
