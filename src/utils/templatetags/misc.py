"""Misc Django template tags."""
from django import template

from yarl import URL

from fakester import __version__

register = template.Library()


@register.simple_tag
def get_version() -> str:
    """Get app version."""
    return f"v{__version__}"


@register.simple_tag
def create_url(scheme: str, domain: str, path: str) -> str:
    """Create URL from passed scheme, domain and path."""
    # Otherwise YARL breaks with:
    # ValueError: Path in a URL with authority should start with a slash ('/') if set
    if not path.startswith("/"):
        path = f"/{path}"

    url = URL.build(scheme=scheme, host=domain, path=path)
    return str(url)
