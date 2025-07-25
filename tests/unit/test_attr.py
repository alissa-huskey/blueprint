import pytest

from blueprint.attr import attr


class Person:
    """Class for testing attrs."""

    age = attr("age")
    color = attr("color", getter=lambda self: "blue")
    limbs = attr("limbs", getter=lambda self: 4, setter=False, deleter=False)

    def _name_setter(self, value):
        self._name = value.upper()
    name = attr("name", setter=_name_setter)


def test_attr_default_getter():
    """
    GIVEN: a class attr using all defaults
    WHEN: an object is instantiated
    THEN: the default getter should work
    """
    person = Person()
    person._age = 23

    assert person.age == 23


def test_attr_default_setter():
    """
    GIVEN: a class attr using all defaults
    WHEN: an object is instantiated
    THEN: the default setter should be work
    """
    person = Person()
    person.age = 42

    assert person.age == 42


def test_attr_default_deleter():
    """
    GIVEN: a class attr using all defaults
    WHEN: an object is instantiated
    THEN: the default deleter should be work
    """
    person = Person()
    person.age = 42
    del person.age

    assert not hasattr(person, "_age")


def test_attr_passed_getter():
    """
    GIVEN: a class attr with a getter is passed
    WHEN: an object is instantiated
    THEN: the passed getter should work
    """
    person = Person()
    person.color = "red"

    assert person.color == "blue"


def test_attr_passed_setter():
    """
    GIVEN: a class attr with a setter is passed
    WHEN: an object is instantiated
    THEN: the passed setter should work
    """
    person = Person()
    person.name = "bill"

    assert person.name == "BILL"


def test_attr_false_doers():
    """
    GIVEN: a class defines attrs with False for some of the doers
    WHEN: an object is instantiated
    THEN: the doers passed in or set to default will work
    AND: the doers set as False should not work
    """
    person = Person()

    assert person.limbs == 4

    with pytest.raises(AttributeError):
        person.limbs = 5

    with pytest.raises(AttributeError):
        del person.limbs
