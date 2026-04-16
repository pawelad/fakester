"""Test `utils.templatetags.misc` module."""

from utils.templatetags.misc import get_version


def test_get_version() -> None:
    """Verifies that `get_version` returns the correct version string."""
    from fakester import __version__

    assert get_version() == f"v{__version__}"
