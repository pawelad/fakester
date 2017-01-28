from django import template

register = template.Library()


@register.assignment_tag
def get_version():
    """Returns app version"""
    from fakester import __version__
    return __version__
