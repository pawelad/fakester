"""
Fakester application misc template tags
"""
from django import template

register = template.Library()


@register.assignment_tag
def get_version():
    """Helper tag for returning app version"""
    from fakester import __version__
    return __version__
