from {{ NAME | to_snake_case }} import __version__


def test_version():
    assert __version__ == "{{ VERSION }}"
