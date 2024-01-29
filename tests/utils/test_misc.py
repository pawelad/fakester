"""Test `utils.misc` module."""

import pytest

from utils.misc import deslugify


@pytest.mark.parametrize(
    ("slug", "title"),
    [
        ("pawelad.html", "Pawelad"),
        ("2023/01/01/this-is-also-a-year.htm", "This is also a year"),
        ("admin/login.php", "Login"),
    ],
)
def test_deslugify(slug: str, title: str) -> None:
    """Creates a reasonable title from the passed slug."""
    assert deslugify(slug) == title
