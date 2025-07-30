from blueprint.dict import Dict


def test_dict():
    obj = Dict()
    assert isinstance(obj, Dict)


def test_dict_attrs():
    obj = Dict({"a": 1})

    assert obj["a"] == 1
    assert obj.a == 1


def test_dict_recursive():
    obj = Dict({"a": {"b": 2}})

    assert obj.a.b == 2


def test_to_dict_recursive():
    a = Dict({"a": {"b": 2}})
    b = a.to_dict()

    assert isinstance(b, dict)
    assert isinstance(b.get("a"), dict)
