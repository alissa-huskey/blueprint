"""Custom base object class."""


class Object():
    """Arbitrary object class."""

    _NO_REPR = []

    def __init__(self, **kwargs):
        """Set all keyword args as attributes."""
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        """Object(attr='value')."""
        attrs = [
            f"{k.lstrip('_')}={v!r}"
            for k, v in self.__dict__.items()
            if k not in self._NO_REPR
        ]
        text = ", ".join(attrs)
        return f"{self.__class__.__name__}({text})"

    def __eq__(self, other):
        """Provide comparison oprators."""
        return (isinstance(other, self.__class__) and
                self.__dict__ == other.__dict__)
