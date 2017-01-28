from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class RedirectsAppConfig(AppConfig):
    name = 'redirects'
    verbose_name = _("redirects")
