"""Custom base object class."""


class Object():
    """Arbitrary object class."""

    def __init__(self, **kwargs):
        """Set all keyword args as attributes."""
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        """Object(attr='value')."""
        attrs = ", ".join([f"{k}={v!r}" for k, v in self.__dict__.items()])
        return f"{self.__class__.__name__}({attrs})"

    def __eq__(self, other):
        """Provide comparison oprators."""
        return (isinstance(other, self.__class__) and
                self.__dict__ == other.__dict__)
