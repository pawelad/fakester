"""Misc Django template tags."""
from django import template

from fakester import __version__

register = template.Library()


@register.simple_tag
def get_version() -> str:
    """Get app version."""
    return f"v{__version__}"
