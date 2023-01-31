"""
Redirects module AppConfig integration.
"""
from django.apps import AppConfig


class RedirectsAppConfig(AppConfig):
    """
    Django AppConfig integration for `redirects` module.
    """

    name = "redirects"
    verbose_name = "redirects"
