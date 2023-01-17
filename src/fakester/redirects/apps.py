"""
Redirects module AppConfig integration.
"""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RedirectsAppConfig(AppConfig):
    """
    Django AppConfig integration for `redirects` module.
    """

    name = "redirects"
    verbose_name = _("redirects")
