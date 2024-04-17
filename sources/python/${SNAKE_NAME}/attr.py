"""attr module."""


class attr():
    """Works like property() except with default getters/setters/deleters."""

    def __new__(cls, name, **kwargs):
        """Return the property for this attribute."""
        obj = object.__new__(cls)
        obj.__init__(name, **kwargs)

        return property(obj.getter, obj.setter, obj.deleter, obj.doc)

    def __init__(self, name, **kwargs):
        """Initialize attr object.

        Arguments:
            name (str): name of the attribute
        Keyword Arguments:
            getter (func): getter function
            setter (func): setter function
            deleter (func): deleter function
            doc (str): docstring
        """
        self.name = name
        self.doc = kwargs.pop("doc", f"{name} attribute")
        self.private_name = f"_{name}"
        self.make_doer_methods(**kwargs)

    def make_doer_methods(self, **kwargs):
        """Assign the getter/setter/deleter attributes on this object."""
        defaults = self.make_defaults()
        for doer in ["getter", "setter", "deleter"]:
            # get the method from either input or default method
            method = kwargs.get(doer, defaults[doer])

            # don't create an accessor if the kwarg value is False
            if method is False:
                method = None

            if callable(method):
                method.__name__ = self.name
                method.__doc__ = self.doc

            # now set the accessor
            setattr(self, doer, method)

    def make_defaults(parent):
        """Generate the default methods."""
        def getter(self):
            self.__dict__.setdefault(parent.private_name, None)
            return getattr(self, parent.private_name)

        def setter(self, value):
            self.__dict__.setdefault(parent.private_name, None)
            setattr(self, parent.private_name, value)

        def deleter(self):
            delattr(self, parent.private_name)

        return {
            "getter": getter,
            "setter": setter,
            "deleter": deleter,
        }
