"""
Redirects application `AppConfig` integration.
"""
from django.apps import AppConfig


class RedirectsConfig(AppConfig):
    """Django `AppConfig` integration for `redirects` application."""

    name = "redirects"
    verbose_name = "Redirects"
